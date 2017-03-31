from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import SignUpSerializer

__all__ = (
    # 'SignUpView',
    # 'ProfileView',
    'SignUp',
    'Login',
)

User = get_user_model()


# class SignUpView(generics.CreateAPIView):
#     serializer_class = SignUpSerializer


class SignUp(APIView):
    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    # permission_classes = (IsAuthenticated,)


    def post(self, request, format=None):
        content = {
            'user': request.user,
            'auth': request.auth,
        }
        print(content)
        return Response(content)

# class ProfileView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def get(self, request, *args, **kwargs):
#         user = request.user
#         serializer = LoginSerializer(user)
#         return Response(serializer.data)
