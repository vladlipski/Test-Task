from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from manager.models import Project, Task
from manager.serializers import TaskSerializer
from manager.helpers import SetupMixin


class CreateTaskTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        Project.objects.create(id=1, title='Test', description='Test',
                               creation_date=date.today())
        self.data =  {
            'title': 'TEST!',
            'description': 'TEST!',
            'due_date': '2018-11-30',
        }

    def test_can_create_task(self):
        response_developer = self.client_developer.post(
            reverse('manager:task-list', kwargs={'project_id': 1}), self.data)
        response_manager = self.client_manager.post(
            reverse('manager:task-list', kwargs={'project_id': 1}), self.data)

        self.assertEqual(response_manager.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)


class ReadTaskTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        project = Project.objects.create(id=1, title='Test',
                                         description='Test', creation_date=date.today())
        Task.objects.create(id=1, title='Test task', description='TEST!',
                                   due_date=date.today(), project=project)

    def test_can_read_task_list(self):
        response_manager = self.client_manager.get(reverse(
            'manager:task-list', kwargs={'project_id': 1}))
        response_developer = self.client_developer.get(reverse(
                'manager:task-list', kwargs={'project_id': 1}))
        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_200_OK)


    def test_can_read_task_detail(self):
        response_manager = self.client_manager.get(
            reverse('manager:task-detail', kwargs={'pk': 1, 'project_id': 1}))
        response_developer = self.client_developer.get(
            reverse('manager:task-detail', kwargs={'pk': 1, 'project_id': 1}))
        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_200_OK)


class UpdateTaskTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        project = Project.objects.create(id=1, title='Test', description='Test',
                                         creation_date=date.today())
        task = Task.objects.create(id=1, title='Test task', description='TEST!',
                                   due_date=date.today(), project_id=project.pk,
                                   performer_id=1)

        self.data = TaskSerializer(task).data
        self.data.update({'title': 'New  title!'})

    def test_can_update_task(self):
        response_manager = self.client_manager.put(
            reverse('manager:task-detail', kwargs={'pk': 1, 'project_id': 1}), self.data)
        response_developer = self.client_developer.put(
            reverse('manager:task-detail', kwargs={'pk': 1, 'project_id': 1}), self.data)

        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)


class DeleteTaskTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        project = Project.objects.create(id=1, title='Test', description='Test', creation_date=date.today())
        Task.objects.create(id=1, title='Test task', description='TEST!',
                                   due_date=date.today(), project=project)

    def test_can_delete_task(self):
        response_developer = self.client_developer.delete(reverse(
            'manager:task-detail', kwargs={'pk': 1, 'project_id': 1}))
        response_manager = self.client_manager.delete(reverse(
            'manager:task-detail', kwargs={'pk': 1, 'project_id': 1}))

        self.assertEqual(response_manager.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)


