from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    status = models.CharField(max_length=255)


class UserSettings(models.Model):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    avatar = models.FileField(null=True, blank=True)


class Voting(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    type = models.IntegerField()
    published = models.DateTimeField()
    finished = models.DateTimeField()
    is_active = models.BooleanField()

    class Meta:
        ordering = ['-finished']


class VoteVariant(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.TextField()


class VoteFact(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    variant = models.ForeignKey(to=VoteVariant, on_delete=models.CASCADE)
    created = models.DateTimeField()


class Complaint(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.IntegerField()


class FavouriteVoting(models.Model):
    author = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)

class VoteImages(models.Model):
    voting = models.ForeignKey(to=Voting, on_delete=models.CASCADE)
    image_url = models.URLField()
