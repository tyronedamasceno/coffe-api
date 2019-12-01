from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from user.views import LoginViewSet

router = routers.DefaultRouter()
router.register('', LoginViewSet, 'login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('core.urls')),
    path('api/v1/users/', include('user.urls')),
    path('api/v1/login/', include(router.urls), name='login'),
]
