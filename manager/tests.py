from datetime import date

from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from manager.models import Project, Task
from manager.serializers import ProjectSerializer, TaskSerializer
from manager.tests_helpers import Helper


class AuthenticationTests(APITestCase):

    def test_required_authentication (self):
        client = APIClient()
        self.assertEqual(client.get('/projects/').status_code, 403)
        self.assertEqual(client.get('/projects/1/tasks/').status_code, 403)
        self.assertEqual(client.get('/users/').status_code, 403)
#
#
#     def test_developer_permissions (self):
#         user = User.objects.create_user('testuser', 'test@gmail.com', password='1111')
#         group = Group.objects.create(name='developer')
#         user.groups.add(group)
#         client = APIClient()
#         client.force_authenticate(user=user)
#         self.assertEqual(client.get('/projects/').status_code, 200)
#         self.assertEqual(client.post('/projects/', {
#             "title": "TEST!",
#             "description": "TEST!",
#             "creation_date": "2017-01-30",
#             "employees": [
#                 23
#             ]
#         }) .status_code, 403)
#         self.assertEqual(client.put('/projects/', {
#             "title": "TEST!",
#             "description": "TEST!",
#             "creation_date": "2017-01-30",
#             "employees": [
#                 23
#             ]
#         }).status_code, 403)
#
#
#     def test_manager_permissions (self):
#         user = Helper.create_manager()
#         client = APIClient()
#         client.force_authenticate(user=user)
#
#         self.assertEqual(client.get('/projects/').status_code, 200)
#
#         self.assertEqual(client.post('/projects/', format='json') .status_code, 201)
#
#         self.assertEqual(client.delete(client.delete('/projects/1').url).status_code,  200)
#
#         self.assertEqual(client.get('/project/1').status_code, 204)


class SetupMixin():

    def set_users(self):
        manager = Helper.create_manager()
        developer = Helper.create_developer()
        self.client_manager = APIClient()
        self.client_developer = APIClient()
        self.client_manager.force_authenticate(user=manager)
        self.client_developer.force_authenticate(user=developer)


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
#

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

    def test_can_delete_user(self):
        response_developer = self.client_developer.delete(reverse(
            'manager:task-detail', kwargs={'pk': 1, 'project_id': 1}))
        response_manager = self.client_manager.delete(reverse(
            'manager:task-detail', kwargs={'pk': 1, 'project_id': 1}))

        self.assertEqual(response_manager.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)