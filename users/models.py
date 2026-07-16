from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.FileField("avatar_image", upload_to="assets/users/avatars")
    bio = models.TextField
    email = models.EmailField
