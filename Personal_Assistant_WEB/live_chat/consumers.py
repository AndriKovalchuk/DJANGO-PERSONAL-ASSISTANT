import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message
from django.contrib.auth.models import User


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        messages = Message.last_50_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        user = data['from']
        user_user = User.objects.filter(username=user)[0]
        message = Message.objects.create(
            user=user_user,
            content=data['message']
        )

        avatar_url = user_user.profile.avatar.url if hasattr(user_user, 'profile') else None

        content = {
            'command': 'new_message',
            'message': self.message_to_json(message, avatar_url)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            # Fetch the avatar URL for each message user
            avatar_url = message.user.profile.avatar.url if hasattr(message.user, 'profile') else None
            result.append(self.message_to_json(message, avatar_url))
        return result

    def message_to_json(self, message, avatar_url):
        return {
            'user': message.user.username,
            'content': message.content,
            'timestamp': str(message.timestamp),
            'avatar_url': avatar_url
        }

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message
    }

    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "chat_message",
             "message": message
             }
        )

    def send_message(self, message):
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
