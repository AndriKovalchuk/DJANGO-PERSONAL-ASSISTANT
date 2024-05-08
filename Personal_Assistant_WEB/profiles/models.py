from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='profile_avatars/default_avatar.png', upload_to='profile_avatars/')
    occupation = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)

    class Meta:
        db_table = 'profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)  # noqa
        print(f'SELF.AVATAR.PATH: {self.avatar.path}')  # noqa

        if img.height > 250 or img.width > 250:
            new_img = (250, 250)
            img.thumbnail(new_img)
            img.save(self.avatar.path)  # noqa


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])  # noqa


class Avatar(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='avatars')
    created_at = models.DateTimeField(default=timezone.now)
    url = models.URLField()

    class Meta:
        db_table = "avatars"
