from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import CoffeType
from core.serializers import CoffeTypeSerializer


class CoffeTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CoffeTypeSerializer
    queryset = CoffeType.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
