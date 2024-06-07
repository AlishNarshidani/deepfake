from django import forms
from django.core.exceptions import ValidationError

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class AudioUploadForm(forms.Form):
    audio = forms.FileField()

    def clean_audio(self):
        file = self.cleaned_data.get('audio')
        if file:
            if not file.content_type.startswith('audio'):
                raise ValidationError('File type is not audio')
        return file