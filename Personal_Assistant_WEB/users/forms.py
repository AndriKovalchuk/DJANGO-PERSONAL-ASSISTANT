from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import CharField, TextInput, EmailInput, EmailField, PasswordInput
from django import forms

from .models import Profile


class RegistrationForm(UserCreationForm):
    username = CharField(max_length=150, min_length=3, required=True,
                         widget=TextInput(attrs={"class": "form-control"}))

    email = EmailField(max_length=254, required=True,
                       widget=EmailInput(attrs={"class": "form-control"}))

    password1 = CharField(required=True,
                          widget=PasswordInput(attrs={"class": "form-control"}))

    password2 = CharField(required=True,
                          widget=PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput())

    class Meta:
        model = Profile
        fields = ['avatar']
