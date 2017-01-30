from django.contrib.auth.models import User, Group, Permission
from django.test import testcases
from rest_framework import status
from rest_framework.test import APIClient

class SetupMixin():

    def set_users(self):
        manager = Helper.create_manager()
        developer = Helper.create_developer()
        self.client_manager = APIClient()
        self.client_developer = APIClient()
        self.client_manager.force_authenticate(user=manager)
        self.client_developer.force_authenticate(user=developer)


class Helper():

    @staticmethod
    def create_manager():
        user = User.objects.create_user('testuser1', 'test@gmail.com', password='1111')
        group = Group.objects.create(name='manager')
        permissions = Permission.objects.filter(codename__in=[
            'add_user', 'change_user', 'delete_user',
            'add_project', 'change_project', 'delete_project',
            'add_task', 'change_task', 'delete_task'
        ])
        for perm in permissions:
            group.permissions.add(perm)
        user.groups.add(group)
        return user

    @staticmethod
    def create_developer():
        user = User.objects.create_user('testuser2', 'test@gmail.com', password='1111')
        group = Group.objects.create(name='developer')
        user.groups.add(group)
        return user


# class GenericCreateTest(SetupMixin, testcases.TestCase):
#     creation_data = {}
#     url = ''
#
#     def setUp(self):
#         self.set_users()
#         self.data = self.creation_data
#
#     def test_can_create_project(self):
#         response_developer = self.client_developer.post(self.url, self.data)
#         response_manager = self.client_manager.post(self.url, self.data)
#
#         self.assertEqual(response_manager.data, status.HTTP_201_CREATED)
#         self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)