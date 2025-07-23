from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

def default_expiry():
    return timezone.now() + timedelta(hours=3)
class UploadedFile(models.Model): # defining a database table. Turns into real table via migrations
    file = models.FileField(upload_to='uploads/') # defines field to store actual file
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE) # connects file to a specific user (uploader) if user deleted then delete files
    uploaded_at = models.DateTimeField(auto_now_add=True) # django autofills timestamp
    expires_at = models.DateTimeField(default=default_expiry)


    def __str__(self): # just for display in django admin or debug
        return f"{self.file.name} uploaded by {self.uploaded_by.username}" # output format
