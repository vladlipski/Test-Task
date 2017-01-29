from django.conf.urls import url, include
from rest_framework import routers

from . import api
from . import views


router = routers.DefaultRouter()
router.register(r'projects', api.ProjectViewSet)
router.register(r'projects/(?P<project_id>[0-9]+)/tasks', api.TaskViewSet)
router.register(r'users', api.UserViewSet)


app_name = 'tasks'
urlpatterns = [
    # url(r'^$', views.AllProjects.as_view(), name='all_projects'),
    # url(r'^project/(?P<pk>[0-9]+)/$', views.DetailProject.as_view(), name='detail_project'),
    # url(r'^project/(?P<pk>[0-9]+)/edit/$', views.UpdateProject.as_view(), name='edit_project'),
    # url(r'^project/create/$', views.CreateProject.as_view(), name='create_project'),
    # url(r'^project/(?P<pk>[0-9]+)/delete/$', views.DeleteProject.as_view(), name='delete_project'),
    #
    # url(r'^project/(?P<project_pk>[0-9]+)/task/create/$', views.CreateTask.as_view(), name='create_task'),
    # url(r'^project/(?P<project_pk>[0-9]+)/task/(?P<pk>[0-9]+)/$', views.DetailTask.as_view(), name='detail_task'),
    url(r'^', include(router.urls)),
]