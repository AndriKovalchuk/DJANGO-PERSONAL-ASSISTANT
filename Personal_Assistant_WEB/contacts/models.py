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
