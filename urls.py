from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('commands/edit', views.edit_commands, name='edit_commands'),
    path('commands/', views.commands, name='commands'),
    path('', views.login_view, name='login'),
]
