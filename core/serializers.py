from rest_framework import serializers

from core.models import CoffeType, Harvest


class CoffeTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoffeType
        fields = ('id', 'name', 'expiration_time')
        read_only_fields = ('id', )


class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = ('id', 'farm', 'bags', 'date', 'coffe_type', 'owner')
        read_only_fields = ('id', )
