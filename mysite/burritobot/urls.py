from django.urls import path
from . import views

urlpatterns = [
    path('authenticated/<str:code>/', views.authenticated, name='authenticated'),
    path('register/', views.register, name='register'),
    path('commands/edit', views.edit_commands, name='edit_commands'),
    path('commands/new', views.new_commands, name='new_commands'),
]