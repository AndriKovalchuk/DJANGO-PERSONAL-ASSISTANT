from . import views
from django.urls import path


app_name = 'filemanager'

urlpatterns = [
    path('file/add/', views.upload_file, name='add_file'),
    path('file/view/', views.uploaded_files, name='uploaded_files'),
    path('file/download/<int:file_id>/', views.download_file, name='download_file'),
    path('file/edit/<int:file_id>/', views.edit_file, name='edit_file'),
    path('file/delete/<int:pk>/', views.delete_file, name='delete_file'),
    
    path('category/add/', views.create_category, name='create_category'),
    path('category/manage/', views.manage_categories, name='manage_categories'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('file/view/<int:category_id>/', views.files_by_categories, name='files_by_categories'),
] 