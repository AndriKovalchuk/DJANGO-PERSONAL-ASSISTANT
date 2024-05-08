from django.contrib.auth.models import User  # noqa
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=25, null=False, unique=True)

    class Meta:
        db_table = "tags"


class Note(models.Model):
    text = models.CharField(null=False)
    description = models.CharField(null=False)
    created = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "notes"
