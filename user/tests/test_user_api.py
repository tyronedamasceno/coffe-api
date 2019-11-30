from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


USER_API_URL = reverse('user:users-list')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successful(self):
        """Test creating user with valid payload successful"""
        payload = {
            'email': 'tyrone@coffeapi.com',
            'password': 'password',
            'name': 'Tyrone'
        }

        response = self.client.post(USER_API_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        payload = {
            'email': 'tyrone@coffeapi.com',
            'password': 'password',
        }
        create_user(**payload)

        response = self.client.post(USER_API_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
