from django.urls import path, include

from rest_framework import routers

from core import views


router = routers.DefaultRouter()
router.register('coffe_types', views.CoffeTypeViewSet, base_name='coffe_types')
router.register('harvests', views.HarvestViewSet, base_name='harvests')
router.register(
    'storage_report', views.StorageReportViewSet, base_name='storage_report'
)

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
]
