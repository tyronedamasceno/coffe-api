from rest_framework import viewsets

from core.models import CoffeType
from core.serializers import CoffeTypeSerializer


class CoffeTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CoffeTypeSerializer
    queryset = CoffeType.objects.all()
