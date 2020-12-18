from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=255)


class UserSettings(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
