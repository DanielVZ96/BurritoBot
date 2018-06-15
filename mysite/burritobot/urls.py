from django.urls import path
from . import views

urlpatterns = [
    path('authenticated/<str:code>/', views.authenticated, name='authenticated'),
    path('register/', views.register, name='register'),
    path('commands/', views.commands, name='commands'),
]