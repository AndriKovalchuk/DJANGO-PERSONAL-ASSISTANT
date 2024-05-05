from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from ..models import User
from ..models import Contact, File


class ContactModelTest(TestCase):
    """Tests for the Contact model."""

    @classmethod
    def setUpTestData(cls):
        # Set up data for the whole TestCase
        cls.user = User.objects.create(username='testuser', email='user@example.com', password='testpass')

    def test_create_contact(self):
        """Test creating a new contact and verifying its properties."""
        contact = Contact.objects.create(
            fullname='John Doe',
            address='123 Elm Street',
            phone='1234567890',
            email='john@example.com',
            birthday='1990-01-01',
            user=self.user
        )
        self.assertEqual(contact.fullname, 'John Doe')
        self.assertEqual(contact.email, 'john@example.com')
        self.assertEqual(contact.user, self.user)

    def test_email_unique(self):
        """Test that the email field must be unique across contacts."""
        Contact.objects.create(
            fullname='Jane Doe',
            address='124 Elm Street',
            phone='1234567891',
            email='jane@example.com',
            birthday='1990-02-01',
            user=self.user
        )
        with self.assertRaises(ValidationError):
            contact = Contact(
                fullname='Jane Smith',
                address='125 Elm Street',
                phone='1234567892',
                email='jane@example.com',
                birthday='1991-03-01',
                user=self.user
            )
            contact.full_clean()  # This will raise a ValidationError because the email is not unique


class FileModelTest(TestCase):
    """Tests for the File model."""
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='fileuser', email='fileuser@example.com', password='filepass')

    def test_file_creation(self):
        """Test creating a new file and verifying its properties."""
        file = File.objects.create(
            url='http://example.com/myfile.pdf',
            name='myfile.pdf',
            user=self.user
        )
        self.assertEqual(file.name, 'myfile.pdf')
        self.assertEqual(file.user, self.user)

    def test_file_str(self):
        """Test the string representation of the File model."""
        file = File.objects.create(
            url='http://example.com/myimage.jpg',
            name='myimage.jpg',
            user=self.user
        )
        self.assertEqual(str(file), 'myimage.jpg')
