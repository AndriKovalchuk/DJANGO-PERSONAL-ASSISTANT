from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [

    path("<str:profile_name>/", views.my_profile, name="my_profile"),
    path("<str:profile_name>/edit_profile/", views.edit_profile, name="edit_profile"),
    path('<str:profile_name>/upload_avatar/', views.upload_avatar, name='upload_avatar'),
]

