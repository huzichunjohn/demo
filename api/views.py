from django.contrib.auth.models import User, Group
from django.http import Http404
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import UserSerializer, GroupSerializer, BlogSerializer
from blog.models import Blog

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ExampleView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
	content = {
	    'user': unicode(request.user),
	    'auth': unicode(request.auth),
	}
	return Response(content)

class BlogList(APIView):
    def get(self, request, format=None):
	blogs = Blog.objects.all()
	serializer = BlogSerializer(blogs, many=True, context={'request': request})
	return Response(serializer.data)

    def post(self, request, format=None):
	serializer = BlogSerializer(data=request.data, context={'request': request})
	if serializer.is_valid():
	    serializer.save()
	    return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogDetail(APIView):
    def get_object(self, pk):
	try:
	    return Blog.objects.get(pk=pk)
	except Blog.DoesNotExist:
	    raise Http404

    def get(self, request, pk, format=None):
	blog = self.get_object(pk)
	serializer = BlogSerializer(blog, context={'request': request})
	return Response(serializer.data)

    def put(self, request, pk, format=None):
	blog = self.get_object(pk)
	serializer = BlogSerializer(blog, data=request.data, context={'request': request})
	if serializer.is_valid():
	    serializer.save()
	    return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
    def delete(self, request, pk, format=None):
	blog = self.get_object(pk)
	blog.delete()
	return Response(status=status.HTTP_204_NO_CONTENT) 
