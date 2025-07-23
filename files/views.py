from django.shortcuts import render, redirect
from django.http import FileResponse, Http404
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
from .models import UploadedFile
import os

@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user  # FIXED
            uploaded_file.save()
            return redirect('upload')  # back to the same page
    else:
        form = UploadFileForm()
    
    user_files = UploadedFile.objects.filter(uploaded_by=request.user)  # FIXED
    return render(request, 'files/upload.html', {
        'form': form,
        'user_files': user_files
    })


@login_required
def secure_download(request, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)

        if uploaded_file.uploaded_by != request.user:
            raise Http404("You don't have permission to access this file.")

        file_path = uploaded_file.file.path
        return FileResponse(open(file_path, 'rb'), as_attachment=True)

    except UploadedFile.DoesNotExist:
        raise Http404("File not found.")
