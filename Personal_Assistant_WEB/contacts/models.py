from django.contrib.auth.models import User  # noqa
from django.db import models


class Contact(models.Model):
    fullname = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=False)
    phone = models.CharField(max_length=15, null=False)
    email = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = "contacts"
