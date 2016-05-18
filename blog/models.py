from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField() 
    owner = models.ForeignKey(User)

    class Meta:
        db_table = u'blog'

    def __unicode__(self):
        return u'%s %s' % (self.title, self.owner.username) 
