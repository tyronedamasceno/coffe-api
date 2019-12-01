from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import CoffeType
from core.serializers import CoffeTypeSerializer

COFFE_TYPE_URL = reverse('core:coffe_types-list')


class CoffeTypeTestCase(TestCase):
    def setUp(self):
        self.coffe_type_a = CoffeType.objects.create(
            name='a', expiration_time=5
        )
        self.coffe_type_b = CoffeType.objects.create(
            name='b', expiration_time=5
        )
        self.client = APIClient()

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
