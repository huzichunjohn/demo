from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class TaskSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
	'task-detail', source='id', read_only=True)

    owner = serializers.SlugRelatedField(
	slug_field='username',
	read_only=True,
	default=serializers.CurrentUserDefault())

    categories = serializers.SlugRelatedField(
	slug_field='name',
	queryset=models.Category.objects.all(),
	many=True)

    class Meta:
	model = models.Task
	fields = ('id', 'name', 'owner', 'categories', 'done')

    def create(self, validated_data):
	categories = validated_data.pop('categories')
	task = models.Task.objects.create(**validated_data)
	task.categories = categories
	return task

class CategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
	model = models.Category
	fields = ('id', 'name', 'tasks')

class MyCategorySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, source='my_tasks')

    class Meta:
	model = models.Category
	fields = ('id', 'name', 'tasks')
