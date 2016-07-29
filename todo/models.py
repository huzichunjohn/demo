from django.db import models
from django.contrib.auth.models import User

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
