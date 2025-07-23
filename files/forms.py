from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    expires_in_hours = forms.IntegerField(
        label="Expires in (hours)",
        required=False,
        min_value=1,
        max_value=168,
        help_text="Number of hours this file should live (default: 3)."
)
    class Meta:
        model = UploadedFile
        fields = ['file']  # Don't include 'expires_at' here

    def save(self, commit=True):
        instance = super().save(commit=False)
        from django.utils import timezone
        from datetime import timedelta

        hours = self.cleaned_data.get('expires_in_hours')
        if not hours:
            hours = 3  # Default

        instance.expires_at = timezone.now() + timedelta(hours=hours)
        if commit:
            instance.save()
        return instance
