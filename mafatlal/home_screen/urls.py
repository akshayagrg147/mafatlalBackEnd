from django.urls import path
from home_screen import views

urlpatterns = [
    path('home', views.home_screen_info),
]
