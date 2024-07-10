from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser

class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('user_image', 'username', 'password', 'password2', 'email', 'phone_number', 'birth', 'address', 'detail_address', 'nickname', 'gender', 'is_superuser')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'user_image',)
