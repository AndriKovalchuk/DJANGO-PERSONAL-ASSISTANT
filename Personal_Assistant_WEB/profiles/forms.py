from django import forms
from .models import Profile, Avatar


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'occupation', 'address', 'birth_date', 'phone_number', 'mobile_number']

        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', "id": "profilePicture"}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', "id": "inputOccupation"}),
            'address': forms.TextInput(attrs={'class': 'form-control', "id": "inputAddress"}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', "id": "inputPhone"}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', "id": "inputMobile"}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', "id": "inputBirthday"}),

        }


class AvatarUploadForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control mt-1'}))

    def __init__(self, user, *args, **kwargs):
        super(AvatarUploadForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Avatar
        fields = ['file']
