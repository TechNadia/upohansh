from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.user_signin, name='signin'),
    path('signout/', views.user_signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('register/', views.signup, name='register'),
]