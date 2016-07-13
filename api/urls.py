from django.conf.urls import include, url
from api import views
from rest_framework import routers
from rest_framework.authtoken import views as token_views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth', token_views.obtain_auth_token),
    url(r'^example/$', views.ExampleView.as_view(), name='example'),
    url(r'^blog/$', views.BlogList.as_view(), name='blog'),
    url(r'^blog/(?P<pk>[0-9]+)/$', views.BlogDetail.as_view(), name='blog-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
