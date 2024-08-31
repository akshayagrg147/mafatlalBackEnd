from django.urls import path
from . import views

urlpatterns = [
    path('organization/', views.Organisation.as_view()),
    path('sub_category/', views.Sub_Category.as_view()),
    path('products/', views.Products.as_view()),

]
