from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from freezegun import freeze_time

from core.models import CoffeType, Harvest
from core.serializers import CoffeTypeSerializer, HarvestSerializer

COFFE_TYPE_URL = reverse('core:coffe_types-list')
HARVEST_URL = reverse('core:harvests-list')
LOGIN_URL = '/api/v1/login/'


def perform_login(email, password, api_client):
    credentials = {'email': email, 'password': password}
    get_user_model().objects.create_user(**credentials)
    response = api_client.post(LOGIN_URL, credentials)
    return response.data.get('token')


class CoffeTypeTestCase(TestCase):
    def setUp(self):
        self.coffe_type_a = CoffeType.objects.create(
            name='a', expiration_time=5
        )
        self.coffe_type_b = CoffeType.objects.create(
            name='b', expiration_time=5
        )
        self.client = APIClient()
        self.token = perform_login(
            'tyrone@coffeapi.com', 'password', self.client
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_endpoint_requires_authentication_token(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get(COFFE_TYPE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_listing_all_coffe_types(self):
        response = self.client.get(COFFE_TYPE_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for coffe_type in (self.coffe_type_a, self.coffe_type_b):
            self.assertIn(CoffeTypeSerializer(coffe_type).data, response.data)

    def test_create_a_new_coffe_type(self):
        payload = {
            'name': 'coffe c',
            'expiration_time': 50
        }

        response = self.client.post(COFFE_TYPE_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CoffeType.objects.count(), 3)

    def test_update_coffe_type(self):
        response = self.client.patch(
            reverse('core:coffe_types-detail', args=[self.coffe_type_a.id]),
            {'expiration_time': 20}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        coffe_type = CoffeType.objects.get(pk=self.coffe_type_a.id)
        self.assertEqual(coffe_type.expiration_time, 20)

    def test_delete_coffe(self):
        response = self.client.delete(
            reverse('core:coffe_types-detail', args=[self.coffe_type_a.id])
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        coffe_type = CoffeType.objects.filter(id=self.coffe_type_a.id).first()
        self.assertIsNone(coffe_type)


@freeze_time('2019-12-01')
class HarvestTestCase(TestCase):
    def setUp(self):
        self.coffe_type = CoffeType.objects.create(name='x', expiration_time=5)
        self.client = APIClient()
        self.token = perform_login(
            'tyrone@coffeapi.com', 'password', self.client
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_listing_only_own_harvests(self):
        user1 = get_user_model().objects.get(email='tyrone@coffeapi.com')
        user2 = get_user_model().objects.create_user(
            email='other_user@coffeapi.com', password='secret_password'
        )

        date_ = datetime(2019, 11, 25).date()
        h1 = Harvest.objects.create(
            farm='Fazendinha', bags=500, date=date_,
            coffe_type=self.coffe_type, owner=user1
        )
        h2 = Harvest.objects.create(
            farm='Fazendona', bags=1000, date=date_,
            coffe_type=self.coffe_type, owner=user1
        )
        h3 = Harvest.objects.create(
            farm='Fazenda', bags=750, date=date_, coffe_type=self.coffe_type,
            owner=user2
        )

        response = self.client.get(HARVEST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(HarvestSerializer(h1).data, response.data)
        self.assertIn(HarvestSerializer(h2).data, response.data)
        self.assertNotIn(HarvestSerializer(h3).data, response.data)
