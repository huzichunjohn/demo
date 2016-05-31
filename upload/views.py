import os
from django.http import HttpResponse
from django.shortcuts import render
from .forms import UploadFileForm

def handle_uploaded_file(f):
    if not os.path.exists('/tmp/upload/'):
	os.mkdir('/tmp/upload/')

    with open('/tmp/upload/' + f.name, 'wb+') as destination:
	for chunk in f.chunks():
	    destination.write(chunk)

def index(request):
    if request.method == "POST":
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid():
	    handle_uploaded_file(request.FILES['file'])
	    return HttpResponse('upload successfully.')
    else:
	form = UploadFileForm()
    return render(request, 'upload/index.html', {'form': form})
