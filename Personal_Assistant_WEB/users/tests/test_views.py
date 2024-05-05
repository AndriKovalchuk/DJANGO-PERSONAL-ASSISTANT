from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewTests(TestCase):
    """Tests for user authentication views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

    def test_register_view(self):
        # Testing GET and POST methods for the registration view
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

        response = self.client.post(reverse('users:register'), {
            'username': 'newuser', 'email': 'newuser@example.com',
            'password1': 'complexpassword', 'password2': 'complexpassword'
        })
        self.assertEqual(response.status_code, 302)  # Assuming a redirect on successful registration

    def test_login_view(self):
        # Testing login functionality
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser', 'password': 'password'
        })
        self.assertRedirects(response, expected_url=reverse('profile'))

    def tearDown(self):
        self.user.delete()
