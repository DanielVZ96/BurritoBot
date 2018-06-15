from django.db import models

class AuthInfo(models.Model):
    access_token = models.CharField()
    refresh_token = models.CharField()
    expiration_date = models.DateField()
    scope = models.CharField()

class Command(models.Model):
    command = models.CharField()
    response = models.CharField()
