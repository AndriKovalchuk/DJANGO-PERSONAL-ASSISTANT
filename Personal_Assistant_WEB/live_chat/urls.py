from django.urls import path

from . import views

app_name = 'live_chat'

urlpatterns = [
    path('', views.chat, name='chat'),
    path("<str:room_name>/", views.room, name="room"),
]
