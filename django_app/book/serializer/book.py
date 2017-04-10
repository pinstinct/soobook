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
            'description',
        )


class MyBookSerializer(serializers.ModelSerializer):
    # mybook = BookSerializer(many=True)

    class Meta:
        model = MyBook
        fields = (
            'id',
            'book_id',
            'updated_date'
            # 'mybook',
            # 'author',
            # 'cover_thumbnail',
            # 'publisher',
            # 'description',
        )
