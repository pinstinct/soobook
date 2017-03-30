from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import SignUpSerializer, LoginSerializer

__all__ = (
    'SignUpView',
    'ProfileView',
)

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer


class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = LoginSerializer(user)
        return Response(serializer.data)
