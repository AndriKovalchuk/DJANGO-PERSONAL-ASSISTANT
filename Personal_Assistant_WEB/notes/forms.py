from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "tagsInput"}))

    class Meta:
        model = Note
        fields = ['text', 'description', 'tags']
        widgets = {
            'text': forms.TextInput(attrs={"class": "form-control", "id": "textInput"}),
            'description': forms.TextInput(attrs={"class": "form-control", "id": "descriptionInput"}),
            'tags': forms.TextInput(attrs={"class": "form-control", "id": "tagInput"})
        }

    def clean_tags(self):
        tags_input = self.cleaned_data['tags']
        if tags_input:
            return tags_input
        else:
            return ""
