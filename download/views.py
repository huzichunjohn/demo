import os
import mimetypes

from django.utils.encoding import smart_str
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, FileResponse

def index(request):
    files = os.listdir("/tmp/upload/")
    return render_to_response("download/index.html", {"files": files}, context_instance=RequestContext(request)) 

def download(request, filename):
    response = HttpResponse(open("/tmp/upload/" + filename, "rb"), content_type=mimetypes.guess_type(filename)[0])
    response["Content-Length"] = os.path.getsize("/tmp/upload/" + filename)
    response["Content-Disposition"] = "attachment; filename=%s" % smart_str(filename)
    response['X-Sendfile'] = smart_str("/tmp/upload/" + filename)
    return response

def download2(request, filename):
    response = FileResponse(open("/tmp/upload/" + filename, "rb"), content_type=mimetypes.guess_type(filename)[0])
    response["Content-Length"] = os.path.getsize("/tmp/upload/" + filename)
    response["Content-Disposition"] = "attachment; filename=%s" % smart_str(filename)
    return response
