from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
#from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse
from .forms import RegistrationForm
from datetime import datetime
import json

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('register_done'))
    kwargs = {}
    kwargs.update(csrf(request))
    kwargs['form'] = RegistrationForm(request.POST)
    return render_to_response('register.html', kwargs)

def register_done(request):
    return render_to_response('register_done.html')

def index(request):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return HttpResponse(json.dumps({"datetime": now}), content_type='application/json')
