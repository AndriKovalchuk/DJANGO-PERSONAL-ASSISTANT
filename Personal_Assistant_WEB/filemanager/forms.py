from django import forms

from .models import Category, File


class FileUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control mt-1'}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(),  # noqa
                                      widget=forms.Select(attrs={'class': 'form-select mt-1'}))

    def __init__(self, user, *args, **kwargs):
        super(FileUploadForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)  # noqa

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
    category = forms.ModelChoiceField(queryset=Category.objects.none(),  # noqa
                                      widget=forms.Select(attrs={'class': 'form-select mt-1'}),
                                      required=False)

    def __init__(self, user, *args, **kwargs):
        super(EditFileForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)  # noqa

    class Meta:
        model = File
        fields = ['name', 'category']
