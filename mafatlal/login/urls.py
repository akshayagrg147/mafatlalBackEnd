from django.urls import path
from . import views

urlpatterns = [
    path('user_login/', views.user_login),
    path('user_register/', views.user_register),
]
