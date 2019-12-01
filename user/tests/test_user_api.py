from copy import copy

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


USER_API_URL = reverse('user:users-list')
LOGIN_URL = '/api/v1/login/'


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload_default = {
            'email': 'tyrone@coffeapi.com',
            'password': 'password',
        }

    def test_create_valid_user_successful(self):
        """Test creating user with valid payload successful"""
        payload = copy(self.payload_default)
        payload['name'] = 'Tyrone'

        response = self.client.post(USER_API_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)
        self.assertIn('name', response.data)

    def test_user_exists(self):
        """Test creating user that already exists fails"""
        create_user(**self.payload_default)

        response = self.client.post(USER_API_URL, self.payload_default)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        create_user(**self.payload_default)

        response = self.client.post(LOGIN_URL, self.payload_default)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_token_invalid_credentials(self):
        """Test token is not created with bad or inexisting credentials"""
        create_user(**self.payload_default)
        bad_payload = copy(self.payload_default)
        bad_payload['password'] = 'wrong_pass'

        response = self.client.post(LOGIN_URL, bad_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

        inexisting_payload = copy(self.payload_default)
        inexisting_payload['email'] = 'wrong@coffeapi.com'

        response = self.client.post(LOGIN_URL, inexisting_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_create_token_missing_field(self):
        """Test that email and password are required to create token"""
        create_user(**self.payload_default)
        no_email = copy(self.payload_default)
        no_email['email'] = ''
        no_password = copy(self.payload_default)
        no_password['password'] = ''

        for payload in (no_email, no_password):
            response = self.client.post(LOGIN_URL, payload)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertNotIn('token', response.data)
