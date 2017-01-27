from django.conf.urls import url
from . import views


app_name = 'tasks'
urlpatterns = [
    url(r'^$', views.AllProjects.as_view(), name='all_projects'),
    url(r'^project/(?P<pk>[0-9]+)/$', views.DetailProject.as_view(), name='detail_project'),
    url(r'^project/(?P<pk>[0-9]+)/edit/$', views.UpdateProject.as_view(), name='edit_project'),
    url(r'^project/create/$', views.CreateProject.as_view(), name='create_project'),
    url(r'^project/(?P<pk>[0-9]+)/delete/$', views.DeleteProject.as_view(), name='delete_project'),

]