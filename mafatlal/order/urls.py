from django.urls import path
from order import views

urlpatterns = [
    path('order_history', views.order_history),
    # path('place_order', views.Order_place),
]