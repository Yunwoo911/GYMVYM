from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser
from django.contrib.auth import update_session_auth_hash

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

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_image', 'username', 'email', 'phone1', 'phone2', 'phone3', 'birth', 'address', 'detail_address', 'nickname', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

        # If you want to apply specific widget attributes for certain fields, you can do so like this:
        self.fields['user_image'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['email'].widget.attrs.update({'readonly': 'readonly'})

class NFCForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['nfc_uid']
