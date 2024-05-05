from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def last_50_messages():
        return Message.objects.order_by('-timestamp').all()[:50]

    class Meta:
        db_table = "messages"
