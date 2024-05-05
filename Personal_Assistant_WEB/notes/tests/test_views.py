from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from notes.models import Note, Tag

class NoteViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='12345')
        self.client.login(username='user1', password='12345')
        self.tag = Tag.objects.create(name='urgent')
        self.note = Note.objects.create(text='Sample Note', description='Sample Description', user=self.user)
        self.note.tags.add(self.tag)

    def test_add_note_view(self):
        response = self.client.get(reverse('notes:add_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notes/add_note.html')

    def test_note_detail_view(self):
        response = self.client.get(reverse('notes:note_detail', args=[self.note.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sample Note')

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('notes:add_note'))
        self.assertRedirects(response, '/accounts/login/?next=/notes/add_note/')
