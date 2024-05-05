import pytest
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from ..views import Contact


@pytest.mark.django_db
class TestContactViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='john', password='doe12345')
        self.contact = Contact.objects.create(
            fullname='Jane Doe',
            address='1234 Street',
            phone='+1234567890',
            email='jane@example.com',
            birthday=timezone.now().date(),
            user=self.user
        )

    def test_contact_list_view(self):
        self.client.login(username='john', password='doe12345')
        response = self.client.get(reverse('contacts:my_contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Jane Doe')

    def test_add_contact_view_get(self):
        self.client.login(username='john', password='doe12345')
        response = self.client.get(reverse('contacts:add_contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/add_contact.html')

    def test_add_contact_view_post_valid(self):
        self.client.login(username='john', password='doe12345')
        response = self.client.post(reverse('contacts:add_contact'), {
            'fullname': 'Sam Smith',
            'address': '4321 Drive',
            'phone': '+0987654321',
            'email': 'sam@example.com',
            'birthday': '1990-05-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Contact.objects.filter(email='sam@example.com').exists())

    def test_edit_contact_view(self):
        self.client.login(username='john', password='doe12345')
        response = self.client.post(reverse('contacts:edit_contact', args=[self.contact.id]), {
            'fullname': 'Jane Doe Updated',
            'address': '1234 Street',
            'phone': '+1234567890',
            'email': 'jane@example.com',
            'birthday': '1990-05-01'
        })
        self.assertEqual(response.status_code, 302)
        self.contact.refresh_from_db()
        self.assertEqual(self.contact.fullname, 'Jane Doe Updated')

    def test_delete_contact_view(self):
        self.client.login(username='john', password='doe12345')
        response = self.client.post(reverse('contacts:delete_contact', args=[self.contact.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Contact.objects.filter(id=self.contact.id).exists())
