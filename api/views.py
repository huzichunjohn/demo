from django.contrib.auth.models import User, Group
from django.http import Http404
from django.shortcuts import render
from django.template.context import RequestContext
from rest_framework import viewsets, status, mixins, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle
from api.serializers import UserSerializer, GroupSerializer, BlogSerializer, TodoSerializer
from blog.models import Blog
from todo.models import Todo
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class OncePerDayUserThrottle(UserRateThrottle):
    rate = '20/day'

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class ExampleView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
	content = {
	    'user': unicode(request.user),
	    'auth': unicode(request.auth),
	}
	return Response(content)

class RestrictedView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
	data = {
	    'id': request.user.id,
	    'username': request.user.username,
	    'token': str(request.auth)
	}
	return Response(data)

class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    throttle_classes = (OncePerDayUserThrottle,)

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

def index(request):
    return render(request, 'api/index.html', context_instance=RequestContext(request))

class ExchangeView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        data = {
            'conversion': 0.00000268
        }
        return Response(data)
