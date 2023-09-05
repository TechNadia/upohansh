from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart, name = 'cart'),
    path('<int:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('decrease/<int:food_id>/', views.decrease_cart, name='decrease_cart'),
    path('increase/<int:food_id>/', views.increase_cart, name='increase_cart'),
] 
