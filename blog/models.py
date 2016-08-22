from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from blog.signals import blog_audit
from crequest.middleware import CrequestMiddleware

class Blog(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    timestamp = models.DateTimeField() 
    owner = models.ForeignKey(User, related_name='blogs')

    class Meta:
        db_table = u'blog'

    def __unicode__(self):
        return u'%s %s' % (self.title, self.owner.username) 

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
	Token.objects.create(user=instance)

class Publication(models.Model):
    title = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('title',)

class Article(models.Model):
    headline = models.CharField(max_length=100)
    publications = models.ManyToManyField(Publication)

    def __unicode__(self):
        return self.headline

    class Meta:
        ordering = ('headline',)

class BlogAudit(models.Model):
    username = models.CharField(max_length=20)
    ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=Blog)
def save_audit_log(sender, instance=None, created=False, **kwargs):
    if created:
        print "add"
    else:
        print "update"

@receiver(post_delete, sender=Blog)
def delete_audit_log(sender, instance=None, **kwargs):
    print instance
    print "delete"

@receiver(blog_audit)
def blog_audit_signal(sender, **kwargs):
    current_request = CrequestMiddleware.get_request()
    ip = current_request.META["REMOTE_ADDR"]
    username = current_request.user.username
    blogaudit = BlogAudit.objects.create(username=username, ip=ip)
    blogaudit.save()

class Syslog(models.Model):
    level = models.CharField(max_length=20)
    message = models.TextField()
    timestamp = models.DateTimeField(blank=True, null=True)
