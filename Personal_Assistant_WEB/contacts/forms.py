import re
from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateTimeInput

from .models import Contact


class ContactForm(ModelForm):
    phone = forms.CharField(max_length=15,
                            widget=forms.TextInput(attrs={"class": "form-control", "id": "phoneInput"}),
                            required=True)

    class Meta:
        model = Contact
        fields = ['fullname', 'address', 'phone', 'email', 'birthday']
        widgets = {
            'fullname': forms.TextInput(attrs={"class": "form-control", "id": "fullnameInput"}),
            'address': forms.TextInput(attrs={"class": "form-control", "id": "addressInput"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "id": "emailInput"}),
            'birthday': DateTimeInput(attrs={"class": "form-control", "id": "birthdayInput"}),
        }

    def birthday_validator(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday > date.today():
            raise ValidationError("Birthday cannot be in the future")
        return birthday

    def phone_validator(self):
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
        birthday = cleaned_data.get('birthday')
        if phone:
            self.phone_validator()
        if birthday:
            self.birthday_validator()
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
