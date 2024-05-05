from django.urls import path
from . import views

app_name = 'contacts'

urlpatterns = [
    path("my_contacts/", views.my_contacts, name="my_contacts"),
    path("add_contact/", views.add_contact, name="add_contact"),
    path('edit_contact/<int:contact_id>/', views.edit_contact, name='edit_contact'),
    path('delete_contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
    path('upcoming_birthdays/', views.upcoming_birthdays, name='upcoming_birthdays'),
    path('search_results_contacts/', views.search_results_contacts, name='search_results_contacts'),
]
