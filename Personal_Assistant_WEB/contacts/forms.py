import re

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateTimeInput

from .models import Contact


class ContactForm(ModelForm):
    phone = forms.CharField(max_length=15,
                            widget=forms.TextInput(attrs={"class": "form-control", "id": "phoneInput"}),
                            )

    class Meta:
        model = Contact
        fields = ['fullname', 'address', 'phone', 'email', 'birthday']
        widgets = {
            'fullname': forms.TextInput(attrs={"class": "form-control", "id": "fullnameInput"}),
            'address': forms.TextInput(attrs={"class": "form-control", "id": "addressInput"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "id": "emailInput"}),
            'birthday': DateTimeInput(attrs={"class": "form-control", "id": "birthdayInput"}),
        }

    def phone_validator(self):
        print("Phone validator method called")
        phone = self.cleaned_data.get('phone')
        regex = r'^\+?1?\d{9,15}$'
        if not re.match(regex, phone):
            raise ValidationError(
                "Phone number must be entered in the following format: '+111111111'. Up to 15 digits allowed."
            )
        return phone

    def clean(self):
        print("Clean method called")
        cleaned_data = super().clean()
        phone = cleaned_data.get('phone')
        if phone:
            self.phone_validator()
        return cleaned_data


class UploadFileForm(forms.Form):
    file = forms.FileField()
