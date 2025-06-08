from django.urls import path
from . import views

urlpatterns = [
    path('', views.foldercon_list, name='foldercon'),
]