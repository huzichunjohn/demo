from django.contrib.auth.models import User, Group
from rest_framework import serializers
from blog.models import Blog

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
	model = User
	fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
	model = Group
	fields = ('url', 'name')

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
	model = Blog
	fields = ('url', 'title', 'body', 'timestamp', 'owner')
