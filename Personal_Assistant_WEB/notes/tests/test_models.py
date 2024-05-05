from django.test import TestCase
from notes.models import Note, Tag
from django.contrib.auth.models import User

class TagModelTest(TestCase):
    def test_string_representation(self):
        tag = Tag(name='personal')
        self.assertEqual(str(tag), tag.name)

class NoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='12345')
        self.tag1 = Tag.objects.create(name='urgent')
        self.tag2 = Tag.objects.create(name='work')
        self.note = Note.objects.create(
            text='Finish the project',
            description='Ensure everything is done',
            user=self.user
        )
        self.note.tags.add(self.tag1, self.tag2)

    def test_note_content(self):
        note = Note.objects.get(id=1)
        self.assertEqual(note.text, 'Finish the project')
        self.assertEqual(note.description, 'Ensure everything is done')
        self.assertEqual(note.user.username, 'user1')
        self.assertEqual(list(note.tags.all()), [self.tag1, self.tag2])
        