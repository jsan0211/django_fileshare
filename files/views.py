from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm

@login_required
def upload_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user
            uploaded_file.save()
            return redirect('upload-success')  # You can make this a “Success” page or back to profile
    else:
        form = UploadFileForm()
    return render(request, 'files/upload.html', {'form': form})
