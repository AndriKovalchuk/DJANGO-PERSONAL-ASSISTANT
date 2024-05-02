from django.shortcuts import render


def chat_view(request):
    return render(request, 'live_chat/chat.html')
