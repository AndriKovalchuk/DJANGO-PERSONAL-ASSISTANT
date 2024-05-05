from django.test import TestCase
from notes.forms import NoteForm

class NoteFormTest(TestCase):
    def test_note_form_valid_data(self):
        form_data = {'text': 'Test Note', 'description': 'Just a test', 'tags': 'test1, test2'}
        form = NoteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_note_form_invalid_data(self):
        form = NoteForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
