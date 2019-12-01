from django.urls import path, include

from rest_framework import routers

from core import views


router = routers.DefaultRouter()
router.register('coffe_types', views.CoffeTypeViewSet, base_name='coffe_types')

app_name = 'core'

urlpatterns = [
    path('', include(router.urls)),
]
