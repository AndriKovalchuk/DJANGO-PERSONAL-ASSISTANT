from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.forms import (CharField, EmailField, EmailInput, PasswordInput,
                          TextInput)


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


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', "id": "inputUsername"}),
        'first_name': forms.TextInput(attrs={'class': 'form-control', "id": "firstName"}),
        'last_name': forms.TextInput(attrs={'class': 'form-control', "id": "lastName"}),
    }
