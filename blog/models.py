from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken.models import Token
from blog.signals import blog_audit
from crequest.middleware import CrequestMiddleware
from audit_log.models.managers import AuditLog

ACTION_CREATE = 1
ACTION_EDIT = 2
ACTION_DELETE = 3

ACTION_CHOICES = (
    (ACTION_CREATE, 'created'),
    (ACTION_EDIT, 'modified'),
    (ACTION_DELETE, 'deleted')
)

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

class Product(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(max_digits=4, decimal_places=2)

    audit_log = AuditLog()

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __unicode__(self):
        return u'{0} - {1} ({2})'.format(self.name, self.description, self.price)

    def get_absolute_url(self):
        return reverse('blog:product_detail', args=[self.pk])

class UserActionManager(models.Manager):

    def log_action(self, user, obj, action, message):
        self.model.objects.create(
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.pk,
            user=user,
            action=action,
            message=message,
        )

    def log_create(self, user, obj, message=''):
        self.log_action(user, obj, ACTION_CREATE, message)

    def log_edit(self, user, obj, message=''):
        self.log_action(user, obj, ACTION_EDIT, message)

    def log_delete(self, user, obj, message=''):
        self.log_action(user, obj, ACTION_DELETE, message) 

class UserAction(models.Model):
    time = models.DateTimeField(auto_now_add=True, editable=False)
    user = models.ForeignKey(User, related_name='actions', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES)
    message = models.TextField(blank=True)

    objects = UserActionManager()

    class Meta:
        ordering = ['-time']

    def __unicode__(self):
        if self.message:
            return u'{0} {1}'.format(self.user, self.message)
        return u'{0} {1} {2}'.format(self.user, self.get_action_display(), self.content_type)

    def icon(self):
        if self.action == ACTION_CREATE:
            return 'red'
        elif self.action == ACTION_EDIT:
            return 'green'
        elif self.action == ACTION_DELETE:
            return 'blue'
        else:
            return ''
