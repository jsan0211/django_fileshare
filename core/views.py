from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from files.models import UploadedFile
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()         # creates the new user
            login(request, user)       # logs them in immediately
            return redirect('home')    # send to homepage
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def home(request):
    return render(request, 'core/home.html')

from django.utils import timezone
from files.models import UploadedFile

@login_required
def profile(request):
    # Delete expired files for this user
    UploadedFile.objects.filter(
        uploaded_by=request.user,
        expires_at__lt=timezone.now()
    ).delete()

    user_files = UploadedFile.objects.filter(uploaded_by=request.user)
    return render(request, 'core/profile.html', {'user_files': user_files})
