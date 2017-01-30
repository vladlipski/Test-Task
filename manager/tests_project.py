from datetime import date

from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from manager.models import Project, Task
from manager.serializers import ProjectSerializer, TaskSerializer, UserSerializer
from manager.helpers import SetupMixin


class CreateProjectTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        self.data =  {
            'id': 1,
            'title': 'TEST!',
            'description': 'TEST!',
            'creation_date': '2017-01-30'
        }

    def test_can_create_project(self):
        response_developer = self.client_developer.post(reverse(
            'manager:project-list'), self.data)
        response_manager = self.client_manager.post(reverse(
            'manager:project-list'), self.data)

        self.assertEqual(response_manager.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)


class ReadProjectTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        Project.objects.create(id=1, title='Test', description='Test',
                               creation_date=date.today())

    def test_can_read_project_list(self):
        response_manager = self.client_manager.get(reverse(
            'manager:project-list'))
        response_developer = self.client_developer.get(reverse(
            'manager:project-list'))

        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_200_OK)

    def test_can_read_project_detail(self):
        response_manager = self.client_manager.get(reverse(
            'manager:project-detail', args=[1]))
        response_developer = self.client_developer.get(reverse(
            'manager:project-detail', args=[1]))

        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_200_OK)


class UpdateProjectTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        project = Project.objects.create(id=1, title='Test',
                                         description='Test', creation_date=date.today())
        self.data = ProjectSerializer(project).data
        self.data.update({'title': 'New  title!'})

    def test_can_update_project(self):
        response_manager = self.client_manager.put(reverse(
            'manager:project-detail', args=[1]), self.data)
        response_developer = self.client_developer.put(reverse(
                'manager:project-detail', args=[1]), self.data)

        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)


class DeleteProjectTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        Project.objects.create(id=1, title='Test', description='Test',
                               creation_date=date.today())

    def test_can_delete_project(self):
        response_developer = self.client_developer.delete(
            reverse('manager:project-detail', args=[1]))
        response_manager = self.client_manager.delete(
            reverse('manager:project-detail', args=[1]))

        self.assertEqual(response_manager.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)

