from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import SignUpSerializer, LoginSerializer, TokenSerializer

__all__ = (
    'SignUpLogin',
    'SignUp',
    'Login',
    'Logout'
)

User = get_user_model()


class SignUpLogin(APIView):
    pass


class SignUp(APIView):
    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        token_model = Token
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, _ = token_model.objects.get_or_create(user=user)
            serializer_token = TokenSerializer(instance=token)
        return Response(serializer_token.data, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            request.auth.delete()
        except (AttributeError, ObjectDoesNotExist):
            return Response({'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        logout(request)
        return Response({"detail": "Successfully logged out."},
                        status=status.HTTP_200_OK)
