from datetime import datetime, timedelta

from django.test import TestCase

from freezegun import freeze_time

from core.models import CoffeType, Harvest, User


@freeze_time('2019-12-01')
class CoffeModelsTestCase(TestCase):
    def setUp(self):
        self.default_user = User.objects.create(
            email='tyrone@coffeapi.com',
            password='password'
        )

    def test_create_coffe_type_and_a_harvest(self):
        """Test that is possible to create instances"""
        conilon = CoffeType.objects.create(name='Conilon', expiration_time=10)
        arabica = CoffeType.objects.create(name='Arabica', expiration_time=5)

        now = datetime.now()
        yesterday = now - timedelta(days=1)

        Harvest.objects.create(
            farm='Fazenda Tamoatá', bags=1000, date=now, coffe_type=arabica,
            owner=self.default_user
        )
        Harvest.objects.create(
            farm='Fazenda Bezerrinho', bags=600, date=yesterday,
            coffe_type=conilon, owner=self.default_user
        )

        self.assertEqual(CoffeType.objects.count(), 2)
        self.assertEqual(Harvest.objects.count(), 2)
        self.assertEqual(self.default_user.harvests.count(), 2)

    def test_check_coffe_expiration_time(self):
        """Test the coffe lifetime checking"""
        conilon = CoffeType.objects.create(name='Conilon', expiration_time=10)

        non_expired_date = datetime.now() - timedelta(days=9)
        expired_date = datetime.now() - timedelta(days=11)

        Harvest.objects.create(
            farm='Fazendinha', bags=500, date=non_expired_date,
            coffe_type=conilon, owner=self.default_user
        )

        Harvest.objects.create(
            farm='Fazendinha', bags=500, date=expired_date,
            coffe_type=conilon, owner=self.default_user
        )

        harvests = Harvest.objects.all()
        non_expired_harvests = len([h for h in harvests if not h.expired])
        self.assertEqual(non_expired_harvests, 1)
