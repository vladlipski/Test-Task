from django.conf.urls import url, include
from rest_framework import routers

from . import api


router = routers.DefaultRouter()
router.register(r'projects', api.ProjectViewSet)
router.register(r'projects/(?P<project_id>[0-9]+)/tasks', api.TaskViewSet)
router.register(r'users', api.UserViewSet)


app_name = 'manager'
urlpatterns = [
    url(r'^', include(router.urls)),
]