from django.contrib.admin import AdminSite
from django.contrib import admin
from .models import Type, Category, FolderCon, ReportFile

class MyAdminSite(AdminSite):
    site_header = "FolderCon Admin"
    site_title = "FolderCon"
    index_title = "Welcome to FolderCon Admin"

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        for app in app_list:
            app['models'].sort(key=lambda x: ['Type', 'Category', 'FolderCon', 'ReportFile'].index(x['object_name']))
        return app_list

admin_site = MyAdminSite(name='myadmin')

class TypeAdmin(admin.ModelAdmin):
    list_display = ('title', 'ico')
    search_fields = ('title',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'slug')
    list_filter = ('type',)
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

class FolderContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'ico', 'png', 'icns', 'zip', 'webp')
    list_filter = ('category',)
    search_fields = ('title',)
class ReportFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'foldercon')
    list_filter = ('foldercon',)
    search_fields = ('title', 'issue_text')

# ثبت مدل‌ها با ادمین سفارشی
admin_site.register(Type, TypeAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(FolderCon, FolderContentAdmin)
admin_site.register(ReportFile, ReportFileAdmin)
