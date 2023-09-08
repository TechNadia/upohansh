from django.urls import path
from . import views
from .views import CustomPasswordChangeView


urlpatterns = [
    path('signin/', views.user_signin, name='signin'),
    path('signout/', views.user_signout, name='signout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.signup, name='register'),
    path('change_password/', CustomPasswordChangeView.as_view(), name='change_password'),
    path('password_change_done/', views.password_change_done, name='password_change_done'),
    path('order_history/', views.order_history, name='order_history'),
    path('trace_order/', views.trace_order, name='trace_order'),
    path('order_details/<int:order_id>/', views.order_details, name='order_details'),
]