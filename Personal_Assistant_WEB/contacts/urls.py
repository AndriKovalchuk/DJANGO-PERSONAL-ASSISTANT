from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path('', views.main, name='main'),
    path('contact/', views.contact, name='contact'),
    path('note/', views.note, name='note'),

    path("add_contact/", views.add_contact, name="add_contact"),
    path("add_note/", views.add_note, name="add_note"),

    path("my_contacts/", views.my_contacts, name="my_contacts"),
    path("my_notes/", views.my_notes, name="my_notes"),

    path('delete_contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('edit_contact/<int:contact_id>/', views.edit_contact, name='edit_contact'),
]
