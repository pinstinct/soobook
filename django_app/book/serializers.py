from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.models import Book

__all__ = (
    'BookSerializer',
    'MyBookAddSerializer',
)

User = get_user_model()


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = (
            'id',
            'title',
            'author',
            'cover_thumbnail',
            'publisher',
            'description',
        )


class MyBookSerializer(serializers.ModelSerializer):
    pass
