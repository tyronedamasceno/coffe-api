from rest_framework import viewsets
# from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.response import Response
from rest_framework.settings import api_settings

from user.models import User
from user.serializers import UserSerializer, AuthTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create  a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

# class CustomAuthToken(ObtainAuthToken):
#     serializer_class = AuthTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data,
#             context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data['user']
#         token, _ = Token.objects.get_or_create(user=user)

#         return Response({'token': token})


# class LoginViewSet(viewsets.ViewSet):
#     """Checks email and password and return an auth token."""

#     def create(self, request):
#         """Use the ObtainAuthToken APIView to validate and create a token."""
#         return CustomAuthToken().post(request)
