from django import forms

from .models import Note


class NoteForm(forms.ModelForm):
    tags = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "exampleInputQuote2"}))

    class Meta:
        model = Note
        fields = ['text', 'description', 'tags']
        widgets = {
            'text': forms.TextInput(attrs={"class": "form-control", "id": "textInput"}),
            'description': forms.TextInput(attrs={"class": "form-control", "id": "descriptionInput"}),
            'tags': forms.TextInput(attrs={"class": "form-control", "id": "tagInput"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def clean_tags(self):
            tags_input = self.cleaned_data['tags']
            if tags_input:
                tags_list = [tag.strip() for tag in tags_input.split(',')]
                return tags_list
            else:
                return []
