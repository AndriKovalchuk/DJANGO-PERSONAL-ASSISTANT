from django.conf import settings
from django.conf.urls.i18n import i18n_patterns, set_language
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns(
    path('', views.main, name='main'),
    path('contacts/', include('contacts.urls')),
    path('notes/', include('notes.urls')),
    path('users/', include('users.urls')),
    path('news/', include('news.urls')),
    path('filemanager/', include('filemanager.urls')),
    path('set-language/', set_language, name='set_language'),
    path('chat/', include('live_chat.urls')),
    path('profiles/', include('profiles.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
