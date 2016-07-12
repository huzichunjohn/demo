from django.conf.urls import include, url
from api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^example/$', views.ExampleView.as_view(), name='example'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
