"""
Views for the user API
"""
from rest_framework import generics,authentication,permissions
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .serailizers import UserSerializer,AuthTokenSerializer

class CreateUserView(generics.CreateAPIView):
    serializer_class=UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create new auth token vor user."""
    serializer_class=AuthTokenSerializer
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class=UserSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
        """Retrive and return the authenication user"""
        return self.request.user