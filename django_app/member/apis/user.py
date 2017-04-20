import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, DEFAULT_FROM_MAIL
from member.serializers import SignUpSerializer, LoginSerializer, TokenSerializer, ActivationSerializer

__all__ = (
    'SignUpLogin',
    'SignUp',
    'Login',
    'Logout',
    'Activate'
)

User = get_user_model()


class SignUpLogin(APIView):
    pass


class SignUp(APIView):
    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = request.POST['username']
            serializer.save()
            send_email(username)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Activate(APIView):
    def get(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({"detail": "Successfully Activation"}, status=status.HTTP_200_OK)


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



def send_email(username):
    text = 'Hi!\nHow are you?\nHere is the link to activate your account:\nhttp://127.0.0.1:8000/api/user/activate?id={}'.format(
        username)
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    msg = MIMEMultipart('alternative')
    msg.attach(part1)
    subject = 'Activate your account at Family Host'
    msg = """\From: {}\nTo: {}\nSubject: {}\n\n{}""".format(DEFAULT_FROM_MAIL, username, subject, msg.as_string())
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server.sendmail(DEFAULT_FROM_MAIL, [username], msg)
    server.quit()
