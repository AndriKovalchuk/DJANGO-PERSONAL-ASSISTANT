from django.test import TestCase
from ..models import User


class UserModelTest(TestCase):
    """Tests for the custom User model."""

    def test_user_creation(self):
        # Creating a user instance to test object creation and field assignment
        user = User.objects.create(
            username='testuser', email='test@example.com', password='securepassword',
            avatar='path/to/avatar.jpg', confirmed=True)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.confirmed)

    def test_user_str_representation(self):
        # Testing the string representation of the User model (if applicable)
        user = User(username='testuser')
        self.assertEqual(str(user), user.username)
