from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'nickname',
        )


class TokenSerializer(serializers.ModelSerializer):
    user = MyUserSerializer()

    class Meta:
        model = Token
        fields = (
            'key',
            'user',
        )


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        min_length=6,
    )

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'nickname',
            'password',
            'is_active',
        )

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        instance.is_active = False
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.EmailField(required=True, allow_blank=True)
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                    if not user.is_active:
                        msg = _('User account is disabled.')
                        raise exceptions.ValidationError(msg)
        else:
            msg = _('Incorrect ID or Password')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs


