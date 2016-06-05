from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import BlogForm
from .models import Blog

from datetime import datetime
from pytz import timezone
import StringIO
import xlsxwriter

@login_required
def index(request):
    #if request.user.is_superuser:
    #    blogs = Blog.objects.all()
    #else:
    #    blogs = Blog.objects.filter(owner__username__exact=request.user)
    blog_list = Blog.objects.all().order_by('-timestamp')
    paginator = Paginator(blog_list, 5)

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render_to_response("blog/index.html", {'blogs': blogs}, context_instance=RequestContext(request))

def hello(request):
    return HttpResponse("Hello world.")

@login_required
def add(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
    	    return HttpResponseRedirect(reverse('blog:index'))    
    else:
        form = BlogForm()
    return render_to_response('blog/add.html', {"form": form}, context_instance=RequestContext(request))

@login_required 
def edit(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        raise Http404

    if request.user.username != blog.owner.username and not request.user.is_superuser:
       return HttpResponseRedirect(reverse('index')) 
   
    blog.timestamp = datetime.now()

    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
	form = BlogForm(instance=blog)
    return render_to_response('blog/edit.html', {"form": form, "blog": blog}, context_instance=RequestContext(request)) 

@login_required
def delete(request, id):
    if request.method == "POST":
        try:
            blog = Blog.objects.get(pk=id)
        except Blog.DoesNotExist:
            raise Http404
    
        if request.user.username != blog.owner.username and not request.user.is_superuser:
            return HttpResponseRedirect(reverse('index'))
    
        blog.delete()
        return HttpResponse("delete blog %s successful." % (id))
    return HttpResponse("the Get method is not supported, use Post.")

@login_required
def download(request):
    blogs = Blog.objects.all()

    buffer = StringIO.StringIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet("Blog")

    worksheet.write_string(0, 0, "title")
    worksheet.write_string(0, 1, "timestamp")
    worksheet.write_string(0, 2, "username")

    for index, blog in enumerate(blogs):
	worksheet.write_string(index+1, 0, blog.title)
	worksheet.write(index+1, 1, blog.timestamp.strftime("%Y-%m-%d"))
	worksheet.write_string(index+1, 2, blog.owner.username)
    workbook.close()

    output = buffer.getvalue()    
    response = HttpResponse(content_type="application/vnd.ms-excel")
    response['Content-Disposition'] = 'attachment; filename=blog.xlsx'
    response.write(output)
    return response
