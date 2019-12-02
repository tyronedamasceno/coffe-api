from django.db.models import Sum

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import CoffeType, Harvest
from core.serializers import (
    CoffeTypeSerializer, HarvestSerializer, StorageReportSerializer
)
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


class StorageReportViewSet(viewsets.GenericViewSet):
    queryset = Harvest.objects.all()
    serializer_class = StorageReportSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(owner=request.user)

        total_bags = queryset.aggregate(Sum('bags'))
        total_bags = total_bags['bags__sum']
        expired_bags = sum([h.bags for h in queryset if h.expired])
        non_expired_bags = total_bags - expired_bags

        origin_farms = queryset.values('farm').distinct()
        origin_farms = [_['farm'] for _ in origin_farms]

        coffe_types = queryset.values('coffe_type').distinct()
        coffe_types = [_['coffe_type'] for _ in coffe_types]

        data = {
            'total_bags': total_bags,
            'non_expired_bags': non_expired_bags,
            'expired_bags': expired_bags,
            'origin_farms': origin_farms,
            'coffe_types': coffe_types,
        }
        serializer = StorageReportSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)
