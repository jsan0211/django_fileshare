from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file_view, name='upload'),
    path('download/<int:file_id>/', views.secure_download, name='secure_download'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('share/<int:file_id>/', views.share_file, name='share_file'),
    path('api/upload/', views.api_upload_file, name='api_upload_file'),
]
