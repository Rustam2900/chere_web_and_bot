from django.contrib.auth.handlers.modwsgi import check_password
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from users.models import CustomUser
from users.serializers import UserProfileSerializer


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('registration')

    def test_user_registration(self):
        data = {
            'full_name': 'user_full_name',
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password': 'test_password',
            'user_type': 'legal'
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.filter(username='test_user').exists(), True)
        user = CustomUser.objects.get(username='test_user')
        self.assertEqual(user.check_password(data['password']), True)


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test_user',
            password='test_password'
        )

    def test_user_login(self):
        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': 'test_password',
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_invalid(self):
        url = reverse('login')
        data = {
            'username': 'test_user',
            'password': 'error'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserProfileViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='test_user',
            password='test_password'
        )
        self.client.force_login(user=self.user)

    def test_user_profile(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserProfileSerializer(instance=self.user).data)

    def test_user_profile_update(self):
        url = reverse('profile')
        data = {
            'username': 'new_test_user',
            'email': 'new_test_user@example.com',
        }
        response = self.client.put(url, data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_test_user')
        self.assertEqual(self.user.email, 'new_test_user@example.com')

