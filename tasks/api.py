from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from rest_framework import viewsets

from .models import Project, Task
from . import serializers as tasks_serializers

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = tasks_serializers.ProjectSerializer

    serializer_classes = {
        'list': tasks_serializers.ProjectsListSerializer,
    }

    def get_serializer_class(self):
        print(self.action)
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action ]
        else:
            return tasks_serializers.ProjectSerializer


    # template_names = {
    #     'list': 'tasks/project-list.html',
    #     'retrieve': 'tasks/project-detail.html',
    # }

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response({'serializer': serializer, 'project': instance})

    # def get_serializer_class(self):
    #     if self.action not in self.serializer_classes:
    #         raise ImproperlyConfigured('Wrong action passed')
    #
    #     return self.serializer_classes[self.action]

    # def get_template_names(self):
    #     if self.action not in self.template_names:
    #         raise ImproperlyConfigured('Wrong action passed')
    #     return [self.template_names[self.action]]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()

    serializer_classes = {
        'create': tasks_serializers.CreateTaskSerializer,
        'list': tasks_serializers.TasksListSerializer,
    }

    def get_serializer_class(self):
        print(self.action)
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        else:
            return tasks_serializers.TaskSerializer

    def get_queryset(self):
        project = Project.objects.get(id=self.kwargs['project_id'])
        return project.tasks.all()

    def create(self, request, *args, **kwargs):
        request.data['project'] = self.kwargs['project_id']
        return super().create(request, *args, **kwargs)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    serializer_classes = {
        'create': tasks_serializers.UserSerializer,
        'list': tasks_serializers.UserListSerializer,
    }

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        else:
            return tasks_serializers.UserSerializer