from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CoffeType(models.Model):
    name = models.CharField(max_length=255)
    expiration_time = models.IntegerField()  # Days

    def __str__(self):
        return f'{self.name}'


class Harvest(models.Model):
    farm = models.CharField(max_length=255)
    bags = models.PositiveIntegerField()
    date = models.DateField()
    coffe_type = models.ForeignKey(CoffeType, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='harvests'
    )

    def __str__(self):
        return f'{self.coffe_type}/{self.date.year}'

    @property
    def expired(self):
        days_since_harvest = (datetime.now().date() - self.date).days
        return days_since_harvest > self.coffe_type.expiration_time
