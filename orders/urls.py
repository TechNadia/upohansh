from django.urls import path, include
from . import views

urlpatterns = [    
    path('complete/', views.complete, name = 'complete'),
    path('place_order/', views.place_order, name = 'place_order'),
]