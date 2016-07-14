from django.contrib.auth.models import User, Group
from rest_framework import serializers
from blog.models import Blog

class UserSerializer(serializers.HyperlinkedModelSerializer):
    blogs = serializers.PrimaryKeyRelatedField(many=True, queryset=Blog.objects.all())

    class Meta:
	model = User
	fields = ('url', 'username', 'email', 'groups', 'blogs')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
	model = Group
	fields = ('url', 'name')

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
	model = Blog
	fields = ('url', 'title', 'body', 'timestamp', 'owner')
