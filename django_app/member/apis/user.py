from django.contrib.auth import get_user_model
from rest_framework import generics

from member.serializers import SignUpSerializer

__all__ = (
    'SignUpView',
)

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
