from django.conf.urls import url, patterns

from . import views

urlpatterns = patterns('blog',
    url(r'^$', views.index, name='index'),
    url(r'^download/$', views.download, name='download'),
    url(r'^hello/$', views.hello, name='hello'),
    url(r'^add/$', views.add, name='add'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete, name='delete'),
    url(r'^audit/$', views.audit, name='audit'),
    url(r'product_index/$', views.product_index, name='product_index'),
    url(r'product/(?P<id>[0-9]+)/$', views.product_detail, name='product_detail'),
    url(r'product_add/$', views.product_add, name='product_add'),
    url(r'^product_edit/(?P<id>[0-9]+)/$', views.product_edit, name='product_edit'),
    url(r'^product_delete/(?P<id>[0-9]+)/$', views.product_delete, name='product_delete'),
)
