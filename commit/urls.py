from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('commit',
    url(r'^$', views.index, name='index'),
)
