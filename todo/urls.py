from django.conf.urls import url, patterns, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'task', views.TaskViewSet)

urlpatterns = patterns('todo',
    #url(r'^$', views.home, name='home'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include(
	'rest_framework.urls', namespace='rest_framework')),
)
