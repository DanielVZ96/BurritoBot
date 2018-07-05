from django.db import models
from django.forms import ModelForm

class AuthInfo(models.Model):
    access_token = models.CharField(max_length=200)
    refresh_token = models.CharField(max_length=200)
    expiration_date = models.DateField()
    scope = models.CharField(max_length=500)

    def __str__(self):
        return self.access_token

class Command(models.Model):
    command = models.CharField(max_length=100)
    response = models.CharField(max_length=2000)

    def __str__(self):
        return self.command

class CommandForm(ModelForm):
    class Meta:
        model = Command
        fields = ['command', 'response']
