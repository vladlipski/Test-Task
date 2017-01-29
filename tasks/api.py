from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions

from .decorators import encrypt_password
from .models import Project, Task
from . import serializers as tasks_serializers

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = (DjangoModelPermissions,)

    serializer_classes = {
        'list': tasks_serializers.ProjectsListSerializer,
        'create': tasks_serializers.ProjectSerializer,
        'update': tasks_serializers.ProjectSerializer,
        'partial_update': tasks_serializers.ProjectSerializer,
    }

    def get_serializer_class(self):
        print(self.action)
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        else:
            return tasks_serializers.RetrieveProjectSerializer

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
    permission_classes = (DjangoModelPermissions,)

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
        return Task.objects.filter(project__id=self.kwargs['project_id'])

    def perform_create(self, serializer):
        try:
            project = Project.objects.get(id=self.kwargs['project_id'])
        except Project.DoesNotExist:
            raise ValidationError
        else:
            serializer.validated_data['project'] = project
        serializer.save()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(groups__name='developer')
    permission_classes = (DjangoModelPermissions, )

    create = encrypt_password(viewsets.ModelViewSet.create)

    serializer_classes = {
        'list': tasks_serializers.UserListSerializer,
        'create': tasks_serializers.UserSerializer,
        'update': tasks_serializers.UserSerializer,
        'partial_update': tasks_serializers.UserSerializer,
    }

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        else:
            return tasks_serializers.RetrieveUserSerializer

    def perform_create(self, serializer):
        try:
            group = Group.objects.get(name='developer')
        except Group.DoesNotExist:
            print ("Group of developers does not exist")
        else:
            serializer.validated_data['groups'] = [group.id, ]
        serializer.save()