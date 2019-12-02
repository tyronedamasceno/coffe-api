from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import CoffeType, Harvest
from core.serializers import CoffeTypeSerializer, HarvestSerializer
from core.permissions import RetrieveUpdateItsOwnHarvests


class CoffeTypeViewSet(viewsets.ModelViewSet):
    serializer_class = CoffeTypeSerializer
    queryset = CoffeType.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )


class HarvestViewSet(viewsets.ModelViewSet):
    serializer_class = HarvestSerializer
    queryset = Harvest.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, RetrieveUpdateItsOwnHarvests, )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not request.user.is_staff:
            queryset = queryset.filter(owner=request.user)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
