from django.contrib.auth.models import User, Group
from rest_framework import serializers
from blog.models import Blog
from todo.models import Todo

class UserSerializer(serializers.HyperlinkedModelSerializer):
    blogs = serializers.PrimaryKeyRelatedField(many=True, queryset=Blog.objects.all(), required=False)

    class Meta:
	model = User
	fields = ('id', 'url', 'username', 'password', 'email', 'groups', 'blogs', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
        read_only_fields = ('id', 'is_staff', 'is_superusesr', 'is_active', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(username=validated_data['username'], email=validated_data['email'])
        if password is not None:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
	model = Group
	fields = ('url', 'name')

class BlogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
	model = Blog
	fields = ('url', 'title', 'body', 'timestamp', 'owner')

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        field = ('todo', 'timestamp', 'user', 'priority', 'completed') 
