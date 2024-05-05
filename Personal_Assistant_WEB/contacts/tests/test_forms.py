import pytest
from django.core.exceptions import ValidationError
from ..forms import ContactForm, UploadFileForm


@pytest.mark.django_db
class TestContactForm:
    def test_valid_data(self):
        """ Test form with valid data """
        form_data = {
            'fullname': 'John Doe',
            'address': '1234 Street',
            'phone': '+1234567890',
            'email': 'john@example.com',
            'birthday': '2000-01-01'
        }
        form = ContactForm(data=form_data)
        assert form.is_valid(), "The form should be valid"

    def test_invalid_phone_number(self):
        """ Test form with an invalid phone number """
        form_data = {
            'fullname': 'John Doe',
            'address': '1234 Street',
            'phone': '12345',  # Invalid phone number
            'email': 'john@example.com',
            'birthday': '2000-01-01'
        }
        form = ContactForm(data=form_data)
        assert not form.is_valid(), "The form should not be valid"
        assert 'phone' in form.errors, "There should be an error for the 'phone' field"

    def test_missing_fullname(self):
        """ Test form with missing fullname """
        form_data = {
            'address': '1234 Street',
            'phone': '+1234567890',
            'email': 'john@example.com',
            'birthday': '2000-01-01'
        }
        form = ContactForm(data=form_data)
        assert not form.is_valid(), "The form should not be valid"
        assert 'fullname' in form.errors, "There should be an error for the 'fullname' field"


@pytest.mark.django_db
class TestUploadFileForm:
    def test_file_field(self):
        """ Test upload form with a dummy file """
        form_data = {'file': 'dummy_file'}
        form = UploadFileForm(data={}, files=form_data)
        assert form.is_valid(), "The form should be valid with a file"
