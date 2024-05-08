from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path("my_notes/", views.my_notes, name="my_notes"),
    path("add_note/", views.add_note, name="add_note"),
    path('edit_note/<int:note_id>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:note_id>/', views.delete_note, name='delete_note'),
]
