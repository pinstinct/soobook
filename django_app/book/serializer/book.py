from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.models import Book, MyBook

__all__ = (
    'BookSerializer',
    'MyBookSerializer',
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
            # 'description', # 검색결과에서 제외
        )


class BookDetailSerializer(serializers.ModelSerializer):
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
    book = BookSerializer()

    class Meta:
        model = MyBook
        fields = (
            'user_id',
            'book',
        )


class MyBookDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer()

    class Meta:
        model = MyBook
        fields = (
            'user_id',
            'book',
        )


