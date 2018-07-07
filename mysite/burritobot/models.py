from django.db import models
from django.forms import ModelForm

class AuthInfo(models.Model):

    def __str__(self):
        return self.access_token


class TwitchUser(models.Model):
    twitch_id = models.IntegerField()
    twitch_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expiration_date = models.DateField()
    scope = models.CharField(max_length=500)

    def __str__(self):
        return self.twitch_name


class Command(models.Model):
    command = models.CharField(max_length=100)
    response = models.CharField(max_length=2000)
    user = models.ForeignKey(TwitchUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.command


