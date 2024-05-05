from django.test import TestCase
from ..forms import RegistrationForm, LoginForm


class RegistrationFormTest(TestCase):
    """Tests for the registration form."""

    def test_form_valid(self):
        # Check that the form is valid with correct data
        form_data = {'username': 'newuser', 'email': 'user@example.com',
                     'password1': 'complexpassword', 'password2': 'complexpassword'}
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_if_passwords_mismatch(self):
        # Ensure the form is invalid if passwords do not match
        form_data = {'username': 'newuser', 'email': 'user@example.com',
                     'password1': 'complexpassword', 'password2': 'different'}
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class LoginFormTest(TestCase):
    """Tests for the login form."""

    def test_login_form_valid(self):
        # Testing valid login data
        form_data = {'username': 'existinguser', 'password': 'password123'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
