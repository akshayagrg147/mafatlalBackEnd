from django.urls import path
from home_screen import views

urlpatterns = [
    path('home', views.home_screen_info),
    path('product_info', views.product_info),
    path('product_list', views.home_sub_category_product_info),
    path('product_info_list', views.product_info_list),
    path('address', views.address_operation),
    path('search', views.search_category),
    
]
