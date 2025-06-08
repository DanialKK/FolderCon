from django.shortcuts import render
from .models import Type, FolderCon

def foldercon_list(request):
    query = request.GET.get('q', '')
    selected_type = request.GET.get('type')
    selected_category = request.GET.get('category')

    # چک کن اگر مقدار 'None' یا مقدار نامعتبر بود None بذار
    if selected_type in [None, '', 'None']:
        selected_type = None
    if selected_category in [None, '', 'None']:
        selected_category = None

    # اگر مقدار عددی بود به int تبدیل کن
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

    context = {
        'types': types,
        'foldercons': foldercons,
        'query': query,
        'selected_type': selected_type,
        'selected_category': selected_category,
    }
    return render(request, 'foldercon_list.html', context)
