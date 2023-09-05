from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name='menu'),
    path('detail/<int:food_id>/', views.food_detail, name='detail'),
    path('category/<slug:category_slug>/', views.menu, name='item_by_category'),
    path('specials/', views.specials, name='specials'),
    path('estimate_delivery/<int:location_id>/', views.estimate_delivery, name='estimate_delivery'),
    
]