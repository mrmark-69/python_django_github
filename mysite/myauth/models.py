from django.contrib.auth.models import User
from django.db import models


def avatar_directory_path(instance: User, filename: str) -> str:
    return f"avatars/avatar_{instance.pk}/avatar/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_directory_path)
