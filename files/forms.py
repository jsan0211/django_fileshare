from django import forms
from .models import UploadedFile

# This form lets Django generate the html file input and validation automatically for the UploadFile model

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']
