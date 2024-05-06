from django import forms
from .models import File, Category


from django import forms
import os

class FileUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control mt-1'}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(), widget=forms.Select(attrs={'class': 'form-select mt-1'}))

    def __init__(self, user, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_extension = os.path.splitext(file.name)[1].lower()
            supported_formats = ['.mov', '.mp4', '.avi', '.mkv', '.wmv',
                                 '.jpeg', '.jpg', '.png',
                                 '.pdf', '.docx', '.xlsx',
                                 '.mp3', '.wav']
            if file_extension not in supported_formats:
                raise forms.ValidationError(
                    "Invalid file format. Please upload a file with one of the following extensions: "
                    + ", ".join(supported_formats)
                )
        return file

    class Meta:
        model = File
        fields = ['file', 'category']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Category'}))

    class Meta:
        model = Category
        fields = ['name']


class UploadFileForm(forms.Form):
    file = forms.FileField()

class EditFileForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'New file name'}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(),
                                      widget=forms.Select(attrs={'class': 'form-select mt-1'}),
                                      required=False)

    def __init__(self, user, *args, **kwargs):
        super(EditFileForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = File
        fields = ['name', 'category']