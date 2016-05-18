from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import BlogForm
from .models import Blog

@login_required
def index(request):
    #if request.user.is_superuser:
    #    blogs = Blog.objects.all()
    #else:
    #    blogs = Blog.objects.filter(owner__username__exact=request.user)
    blog_list = Blog.objects.all()
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
    	    return HttpResponseRedirect(reverse('index'))    
    kwargs = {}
    kwargs.update(csrf(request)) 
    kwargs['form'] = BlogForm(request.POST)
    return render_to_response('blog/add.html', kwargs)

@login_required 
def edit(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        raise Http404

    if request.user.username != blog.owner.username and not request.user.is_superuser:
       return HttpResponseRedirect(reverse('index')) 
   
    if request.method == "POST":
        form = BlogForm(request.POST, instance=blog)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('index'))

    kwargs = {}
    kwargs.update(csrf(request))
    kwargs['form'] = BlogForm(instance=blog) 
    kwargs['blog'] = blog
    return render_to_response('blog/edit.html', kwargs) 

@login_required
def delete(request, id):
    return HttpResponse("delete blog %s." % (id))

