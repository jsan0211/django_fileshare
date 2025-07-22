from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

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

@login_required
def profile(request):
    return render(request, 'core/profile.html')