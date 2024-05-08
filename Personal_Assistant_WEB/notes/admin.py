from django.contrib import admin

from .models import Note, Tag

# Register your models here.
admin.site.register(Tag)
admin.site.register(Note)
