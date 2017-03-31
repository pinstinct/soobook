from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


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
        )

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return instance

# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = (
#             'username',
#             'nickname',
#         )
