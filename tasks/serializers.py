from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_framework import fields

from .models import Project, Task

class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username',)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'password')


class RetrieveUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CreateTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ('title', 'description', 'due_date', 'performer')


class TasksListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title',)


class TaskSerializer(serializers.ModelSerializer):


    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'performer')



class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title', 'description', 'creation_date', 'employees')

class ProjectsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'title',)

class RetrieveProjectSerializer(serializers.ModelSerializer):
    tasks = TasksListSerializer(many=True, read_only=True)
    employees = UserListSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'creation_date', 'employees', 'tasks')