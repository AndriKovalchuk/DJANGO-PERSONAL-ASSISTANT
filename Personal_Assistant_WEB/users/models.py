from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    reset_token = models.CharField(max_length=255, null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
