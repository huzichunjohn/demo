from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^blog/', include('blog.urls')),
    url(r'^upload/', include('upload.urls')),
    url(r'^download/', include('download.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', \
        {'next_page': '/accounts/login/'}),
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/done/$', views.register_done, name='register_done'),
    url(r'^admin/', include(admin.site.urls)),
]
