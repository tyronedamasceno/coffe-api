from django.urls import path, include

from rest_framework import routers

from user import views


router = routers.DefaultRouter()
router.register('', views.UserViewSet, base_name='users')

app_name = 'user'

urlpatterns = [
    path('', include(router.urls)),
]
