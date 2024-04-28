from django.db import models

from users.models import User  # noqa


class Contact(models.Model):
    fullname = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=15, null=False)
    email = models.CharField(max_length=50, null=False, unique=True)
    birthday = models.DateField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "contacts"


class File(models.Model):
    url = models.URLField(max_length=200)
    name = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "files"
