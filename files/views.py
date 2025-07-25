from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import UploadFileForm
from .forms import ShareFileForm
from .models import UploadedFile
from datetime import timedelta
import os

@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user

            # Check if expires_at was provided; if not, set default
            if not uploaded_file.expires_at:
                uploaded_file.expires_at = timezone.now() + timedelta(hours=3)

            uploaded_file.save()
            return redirect('upload')  # back to the same page
    else:
        form = UploadFileForm()
    
    user_files = UploadedFile.objects.filter(uploaded_by=request.user)
    return render(request, 'files/upload.html', {
        'form': form,
        'user_files': user_files
    })

@login_required
def secure_download(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)

        if (uploaded_file.uploaded_by != request.user and
            request.user not in uploaded_file.shared_with.all()):
            raise Http404("You don't have permission to access this file.")

        file_path = uploaded_file.file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True)

    except UploadedFile.DoesNotExist:
        raise Http404("File not found.")
    
@login_required
def delete_file(request, file_id):
    # Only allow delete if file belongs to the logged-in user
    file = get_object_or_404(UploadedFile, id=file_id, uploaded_by=request.user)
    
    if request.method == 'POST':
        file.file.delete()   # Deletes the file from disk
        file.delete()        # Deletes the DB record
        return redirect('profile')

    # If GET, show confirmation page
    return render(request, 'files/delete_confirm.html', {'file': file})

@login_required
def share_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id, uploaded_by=request.user)

    if request.method == 'POST':
        form = ShareFileForm(request.POST)
        if form.is_valid():
            user_to_share = form.cleaned_data['username']  # This is a User object

            # --- EDGE CASE 1: Prevent sharing with yourself ---
            if user_to_share == request.user:
                messages.error(request, "You cannot share a file with yourself.")
                return redirect('share_file', file_id=file.id)

            # --- EDGE CASE 2: Prevent duplicate sharing ---
            if file.shared_with.filter(id=user_to_share.id).exists():
                messages.info(request, f"File is already shared with {user_to_share.username}.")
                return redirect('profile')

            # Normal flow: add user to shared_with
            file.shared_with.add(user_to_share)
            messages.success(request, f"File shared with {user_to_share.username}.")
            return redirect('profile')
    else:
        form = ShareFileForm()
    
    return render(request, 'files/share_file.html', {'form': form, 'file': file})
