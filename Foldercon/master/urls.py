# master/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.foldercon_list, name='foldercon'),
    path('foldercon/download/<int:pk>/<str:filetype>/', views.download_folder_file, name='download_folder_file'),
    path('update-report-file/', views.update_report_file, name='update_report_file'),
]
