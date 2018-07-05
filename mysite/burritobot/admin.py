from django.contrib import admin
from .models import Command, AuthInfo

admin.site.register(Command)
admin.site.register(AuthInfo)
