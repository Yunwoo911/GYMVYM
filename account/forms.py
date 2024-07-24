from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid login credentials")
        return cleaned_data

class SignupForm(UserCreationForm):
    user_image = forms.ImageField(required=False)
    birth = forms.DateField(required=True)
    phone1 = forms.CharField(max_length=3, required=True)
    phone2 = forms.CharField(max_length=4, required=True)
    phone3 = forms.CharField(max_length=4, required=True)

    class Meta:
        model = CustomUser
        fields = ('user_image', 'username', 'password1', 'password2', 'email', 'phone1', 'phone2', 'phone3', 'birth', 'address', 'detail_address', 'nickname', 'gender', 'is_superuser')

    def save(self, request, commit=True):
        user = super(SignupForm, self).save(commit=False)
        if self.cleaned_data.get('user_image'):
            user.user_image = self.cleaned_data['user_image']
        if commit:
            user.save()
        return user

class NFCForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nfc_uid']
