from django.urls import path
from . import views

app_name = 'live_chat'


urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
]
