from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=255)


class UserSettings(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)


class Voting(models.Model):
    author = models.IntegerField()
    name = models.CharField()
    description = models.CharField()
    type = models.IntegerField()
    published = models.DateTimeField()
    finished = models.DateTimeField()
    is_active = models.BooleanField()


class VoteVariant(models.Model):
    voting = models.IntegerField()
    description = models.CharField()


class VoteFact(models.Model):
    author = models.IntegerField()
    variant = models.IntegerField()
    created = models.DateTimeField()


class Complaint(models.Model):
    author = models.IntegerField()
    voting = models.IntegerField()
    description = models.CharField()
    status = models.IntegerField()


class Products(models.Model):
    author = models.IntegerField()
    name = models.CharField()
    status = models.CharField()
    created_at = models.CharField()
