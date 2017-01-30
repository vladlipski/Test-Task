from rest_framework.test import APITestCase, APIClient


class AuthenticationTests(APITestCase):

    def test_required_authentication (self):
        client = APIClient()
        self.assertEqual(client.get('/projects/').status_code, 403)
        self.assertEqual(client.get('/projects/1/tasks/').status_code, 403)
        self.assertEqual(client.get('/users/').status_code, 403)