from django.shortcuts import render, get_object_or_404
from django.http import FileResponse, Http404, JsonResponse
from .models import Type, FolderCon, ReportFile
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def foldercon_list(request):
    query = request.GET.get('q', '')
    selected_type = request.GET.get('type')
    selected_category = request.GET.get('category')

    if selected_type in [None, '', 'None']:
        selected_type = None
    if selected_category in [None, '', 'None']:
        selected_category = None

    if selected_type is not None:
        try:
            selected_type = int(selected_type)
        except ValueError:
            selected_type = None

    if selected_category is not None:
        try:
            selected_category = int(selected_category)
        except ValueError:
            selected_category = None

    types = Type.objects.prefetch_related('categories').all()
    foldercons = FolderCon.objects.filter(is_visible=True)

    if query:
        foldercons = foldercons.filter(title__icontains=query)

    if selected_type is not None:
        foldercons = foldercons.filter(category__type__id=selected_type)

    if selected_category is not None:
        foldercons = foldercons.filter(category__id=selected_category)

    # تشخیص درخواست ajax به صورت استاندارد
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for f in foldercons:
            data.append({
                'id': f.id,
                'title': f.title,
                'description': f.description,
                # فیلدهای مورد نیاز خودت را اینجا اضافه کن
            })
        return JsonResponse({'foldercons': data})

    context = {
        'types': types,
        'foldercons': foldercons,
        'query': query,
        'selected_type': selected_type,
        'selected_category': selected_category,
    }
    return render(request, 'foldercon_list.html', context)


def download_folder_file(request, pk, filetype):
    folder = get_object_or_404(FolderCon, pk=pk, is_visible=True)

    valid_filetypes = ['ico', 'png', 'icns', 'zip']
    if filetype not in valid_filetypes:
        raise Http404("file type not valid")

    file_field = getattr(folder, filetype, None)
    if not file_field:
        raise Http404("file not found.")

    if filetype == 'ico':
        folder.ico_downloads += 1
    elif filetype == 'png':
        folder.png_downloads += 1
    elif filetype == 'icns':
        folder.icns_downloads += 1
    elif filetype == 'zip':
        folder.zip_downloads += 1

    folder.save()

    try:
        return FileResponse(file_field.open(), as_attachment=True)
    except FileNotFoundError:
        raise Http404("File not found.")
def update_report_file(request):
    if request.method == "POST":
        foldercon_id = request.POST.get('report_file_id')  # اگر نام این پارامتر اشتباهه، اصلاح کن
        title = request.POST.get('title')
        issue_text = request.POST.get('issue_text')

        try:
            foldercon = FolderCon.objects.get(id=foldercon_id)
        except FolderCon.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'FolderCon not found'}, status=404)

        # ایجاد گزارش جدید برای فولدر
        report = ReportFile.objects.create(
            foldercon=foldercon,
            title=title,
            issue_text=issue_text
        )
        return JsonResponse({'status': 'success', 'message': 'Report saved successfully'})

    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)
