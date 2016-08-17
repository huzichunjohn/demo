from django.conf.urls import include, url
from django.contrib import admin

from . import views
from .views import IndexView

urlpatterns = [
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^get/$', views.get, name='get'),
    url(r'^set/$', views.set, name='set'),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^upload/', include('upload.urls')),
    url(r'^download/', include('download.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', \
        {'next_page': '/accounts/login/'}),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/done/$', views.register_done, name='register_done'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
