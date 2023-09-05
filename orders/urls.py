from django.urls import path, include
from . import views

urlpatterns = [    
    path('place_order/', views.place_order, name = 'place_order'),
    path('checkout/', views.checkout, name = 'checkout'),    
    path('success/', views.success_view, name='success_view'),
]