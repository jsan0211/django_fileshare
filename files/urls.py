from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_file_view, name='upload'),
    path('download/<int:file_id>/', views.secure_download, name='secure_download'),
]
