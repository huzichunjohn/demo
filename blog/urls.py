from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^hello/$', views.hello, name='hello'),
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete, name='delete'),
]
