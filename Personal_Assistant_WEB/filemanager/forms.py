from django import forms
from .models import File, Category


class FileUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control mt-1'}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(),
                                      widget=forms.Select(attrs={'class': 'form-select mt-1'}))

    def __init__(self, user, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)

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
