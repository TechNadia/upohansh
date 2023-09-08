from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CustomPasswordChangeForm(PasswordChangeForm):
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'}))
