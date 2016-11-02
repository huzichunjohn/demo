from django.http import HttpResponse
from django.template import RequestContext
from rest_framework import viewsets
from rest_framework.filters import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from . import serializers, models, filters

from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('todo', 'templates'))

def jinja_render(request, template_name, dictionary=None):
    if not dictionary:
        dictionary = {}
    template = env.get_template(template_name)
    new_context = RequestContext(request, dictionary)
    context_dict = {}
    for d in new_context.dicts:
        context_dict.update(d)

    rendered_template = template.render(**context_dict)
    return HttpResponse(rendered_template)

def home(request):
    return jinja_render(request, "index.html")

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

    @detail_route()
    def mime(self, request, *args, **kwargs):
	category = self.get_object()
	category.my_tasks = category.tasks.filter(
	    owner=request.user)
	serializer = serializers.MyCategory(
	    category,
	    context={'request': request}
	)
	return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = filters.TaskFilter

    def perform_create(self, serializer):
	serializer.save(owner=self.request.user)

    @list_route()
    def mime(self, request):
	queryset = self.filter_queryset(
	    self.get_queryset().filter(owner=request.user))
	serializer = self.get_serializer(queryset, many=True)
	return Response(serializer.data)
