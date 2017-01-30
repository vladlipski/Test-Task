from django.contrib.auth.models import User, Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from manager.serializers import UserSerializer
from manager.helpers import SetupMixin


class CreateUserTest(SetupMixin, APITestCase):
    def setUp(self):
        self.set_users()
        self.data = {
            'username': 'mike',
            'first_name': 'Mike',
            'last_name': 'Tyson',
            'password': '1111'
        }

    def test_can_create_user(self):
        response_developer = self.client_developer.post(reverse(
            'manager:user-list'), self.data)
        response_manager = self.client_manager.post(reverse(
            'manager:user-list'), self.data)

        self.assertEqual(response_manager.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)


class ReadUserTest(SetupMixin, APITestCase):

    def setUp(self):
        self.set_users()
        self.user = User.objects.create(username='mike', first_name='Mike',
                            last_name='Tyson', password='1111')
        self.user.groups.add(Group.objects.get(name='developer'))


    def test_can_read_user_list(self):
        response_manager = self.client_manager.get(reverse(
            'manager:user-list'))
        response_developer = self.client_developer.get(reverse(
            'manager:user-list'))

        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_200_OK)

    def test_can_read_user_detail(self):
        response_manager = self.client_manager.get(reverse(
            'manager:user-detail', args=[self.user.id]))
        response_developer = self.client_developer.get(reverse(
            'manager:user-detail', args=[self.user.id]))

        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_200_OK)


class UpdateUserTest(SetupMixin, APITestCase):
    def setUp(self):
        self.set_users()
        self.user = User.objects.create(username='mike', first_name='Mike',
                                        last_name='Tyson', password='1111')
        self.user.groups.add(Group.objects.get(name='developer'))
        self.data = UserSerializer(self.user).data
        self.data.update({'first_name': 'Changed'})

    def test_can_update_user(self):
        response_manager = self.client_manager.put(reverse(
            'manager:user-detail', args=[self.user.id]), self.data)
        response_developer = self.client_developer.put(reverse(
            'manager:user-detail', args=[self.user.id]), self.data)

        self.assertEqual(response_manager.status_code, status.HTTP_200_OK)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)


class DeleteUserTest(SetupMixin, APITestCase):
    def setUp(self):
        self.set_users()
        self.user = User.objects.create(username='mike', first_name='Mike',
                                        last_name='Tyson', password='1111')
        self.user.groups.add(Group.objects.get(name='developer'))

    def test_can_delete_user(self):
        response_developer = self.client_developer.delete(
            reverse('manager:user-detail', args=[self.user.id]))
        response_manager = self.client_manager.delete(
            reverse('manager:user-detail', args=[self.user.id]))

        self.assertEqual(response_manager.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response_developer.status_code, status.HTTP_403_FORBIDDEN)