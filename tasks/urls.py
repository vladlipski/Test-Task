from django.conf.urls import url
from . import views


app_name = 'tasks'
urlpatterns = [
    url(r'^$', views.AllProjectsView.as_view(), name='all_projects'),
    url(r'^(?P<pk>[0-9]+)/$', views.ProjectView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    #url(r'^accounts/profile/$', views.ProfileView.as_view(), name='profile'),
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]