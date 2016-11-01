from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import BlogForm, ProductForm
from .models import Blog, Product, UserAction

from datetime import datetime
from pytz import timezone
import StringIO
import xlsxwriter
import logging
logger = logging.getLogger("demo")

from metrology import Metrology
import random
import time

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

#@Metrology.timer('hello')
def sleep_random_seconds():
    time.sleep(random.randint(1, 3))

def hello(request):
    sleep_random_seconds()
    logger.error("oh my god.")
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

def audit(request):
    audits = Product.audit_log.all()
    return render_to_response('blog/audit.html', {"audits": audits}, context_instance=RequestContext(request))

@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'blog/product/detail.html', {"product": product})

@login_required
def product_index(request):
    products = Product.objects.all()
    actions = UserAction.objects.all()
    return render_to_response('blog/product/index.html', {'products': products, 'actions': actions}, context_instance=RequestContext(request))

@login_required
def product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()

            msg = u'Created product'
            if hasattr(product, 'get_absolute_url'):
                msg = u'{0} <a href="{1}">{2}</a>'.format(msg, product.get_absolute_url(), product)
            else:
                msg = u'{0} {1}'.format(msg, product)
            UserAction.objects.log_create(request.user, product, msg)
            return HttpResponseRedirect(reverse('blog:product_index'))
    else:
        form = ProductForm()
    return render_to_response('blog/product/add.html', {"form": form}, context_instance=RequestContext(request))

@login_required
def product_edit(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            
            msg = u'Modified product'
            if hasattr(product, 'get_absolute_url'):
                msg = u'{0} <a href="{1}">{2}</a>'.format(msg, product.get_absolute_url(), product)
            else:
                msg = u'{0} {1}'.format(msg, product)
            UserAction.objects.log_edit(request.user, product, msg)

            return HttpResponseRedirect(reverse('blog:product_index'))
    else:
        form = ProductForm(instance=product)

    return render_to_response('blog/product/edit.html', {"form": form, "product": product}, context_instance=RequestContext(request))

@login_required
def product_delete(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        raise Http404
    
    product.delete()

    msg = u'Deleted product {0}'.format(product)
    UserAction.objects.log_delete(request.user, product, msg)

    return HttpResponse("ok")
