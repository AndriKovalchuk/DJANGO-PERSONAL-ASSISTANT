from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.main, name='main'),

    # Contacts
    path("my_contacts/", views.my_contacts, name="my_contacts"),
    path("add_contact/", views.add_contact, name="add_contact"),
    path('edit_contact/<int:contact_id>/', views.edit_contact, name='edit_contact'),
    path('delete_contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),

    # Notes
    path("my_notes/", views.my_notes, name="my_notes"),
    path("add_note/", views.add_note, name="add_note"),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),

    # Search
    path('search_results/', views.search_results, name='search_results'),

    # Files
    path('my_files/', views.my_files, name='my_files'),
    path('download_file/<path:file_url>/', views.download_file, name='download_file'),
    path('upload_file/', views.upload_file, name='upload_file'),

]
