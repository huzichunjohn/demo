from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from . import models

class TestTask(APITestCase):
    def test_task_creation(self):
	user = User.objects.create(username="admin")
	user.set_password("a")
	user.save()
	self.client.login(username="admin", password="a")
	category = models.Category.objects.create(name="Django")
	url = reverse('task-list')
	data = {
	    "name": "demo",
	    "owner": user.username,
	    "categories": [catogory.name],
	    "done": False,
	    "url": "http://testserver/task/1/",
	}
	response = self.client.post(url, data, format='json')
	self.assertEqual(
	    response.status_code, status.HTTP_201_CREATED,
	    reponse.content)
	data['id'] = 1
	self.assetEqual(response.data, data)
	self.assetEqual(catesgory.tasks.count(), 1)
	task = models.Task.objects.get(id=1)
	self.assetEqual(task.owner_id, user.id)
