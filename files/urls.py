from django.urls import path
from . import views
from .views import delete_old_files
urlpatterns = [
    path('upload/', views.file_upload, name='file_upload'),
    path('download/<int:file_id>/', views.file_download, name='file_download'),
    path('share/<int:file_id>/', views.share_file, name='share_file'),
    path('list/', views.file_list, name='file_list'),
    path('download/', views.general_download, name='general_download'),
    path('delete_old_files/', delete_old_files, name='delete_old_files'),
    path('', views.file_interface, name='file_interface'),
]
