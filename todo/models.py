from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from bitfield import BitField

# Create your models here.
class Todo(models.Model):
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Normal'),
        (3, 'Hign')
    )

    todo = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=2)
    completed = models.BooleanField(default=False)

    class Meta:
        db_table = 'todo'
        ordering = ['-priority', 'todo']

    def __unicode__(self):
        return u'%d %s %s' % (self.id, self.todo, self.completed)

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    class Meta:
	verbose_name_plural = "Categories"

class Task(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    categories = models.ManyToManyField(
        Category, related_name="tasks")
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class MyModel(models.Model):
    flags = BitField(flags=(
	('awesome_flag', 'Awesome Flag!'),
	('flaggy_foo', 'Flaggy Foo'),
	('baz_bar', 'Baz (bar)'),
    ))
