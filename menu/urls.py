from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('category/<slug:category_slug>/', views.menu, name='item_by_category'),
]