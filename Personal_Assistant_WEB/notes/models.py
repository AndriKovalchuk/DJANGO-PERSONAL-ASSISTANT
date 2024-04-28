from django.db import models

from users.models import User  # noqa


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    class Meta:
        db_table = "tags"


class Note(models.Model):
    text = models.CharField(null=False)
    description = models.CharField(max_length=150, null=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "notes"
