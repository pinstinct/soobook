from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.models import Book, MyBook
from book.serializer import StarSerializer, BookCommentSerializer, BookMarkSerializer

__all__ = (
    'BookSerializer',
    'MyBookSerializer',
    'MyBookDetailSerializer',
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
    mybook_id = serializers.IntegerField(source='id')
    book = BookSerializer()
    comment = BookCommentSerializer(many=True, source='bookcomment_set')
    star = StarSerializer(many=True, source='bookstar_set')
    mark = BookMarkSerializer(many=True, source='bookmark_set')

    class Meta:
        model = MyBook
        fields = (
            'mybook_id',
            'updated_date',
            'book',
            'comment',
            'star',
            'mark',
        )


class MyBookDetailSerializer(serializers.ModelSerializer):
    mybook_id = serializers.IntegerField(source='id')
    book = BookSerializer()
    comment = BookCommentSerializer(many=True, source='bookcomment_set')
    star = StarSerializer(many=True, source='bookstar_set')
    mark = BookMarkSerializer(many=True, source='bookmark_set')

    class Meta:
        model = MyBook
        fields = (
            'mybook_id',
            'updated_date',
            'book',
            'comment',
            'star',
            'mark',
        )
