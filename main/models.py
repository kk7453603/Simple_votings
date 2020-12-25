from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=255)
    USERNAME_FIELD = models.CharField(max_length=30, unique=False, default="anonim")
    password = models.TextField()
    email = models.EmailField()
    avatar = models.FileField(default="none")
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField()

class UserSettings(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)


class Voting(models.Model):
    author = models.IntegerField()
    name = models.TextField()
    author_name = models.ForeignKey(to=User, on_delete=models.CASCADE)
    description = models.TextField()
    type = models.IntegerField()
    published = models.DateTimeField()
    finished = models.DateTimeField()
    is_active = models.BooleanField()


class VoteVariant(models.Model):
    voting = models.IntegerField()
    description = models.TextField()


class VoteFact(models.Model):
    author = models.IntegerField()
    variant = models.IntegerField()
    created = models.DateTimeField()


class Complaint(models.Model):
    author = models.IntegerField()
    voting = models.IntegerField()
    description = models.TextField()
    status = models.IntegerField()


class FavouriteVoting(models.Model):
    author = models.IntegerField()
    voting = models.IntegerField()
