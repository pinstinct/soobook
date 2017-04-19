from rest_framework import serializers

from book.models import BookStar, Book

__all__ = (
    'StarSerializer',
    'StarListSerializer',
)


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStar
        fields = (
            'id',
            'content',
            'updated_date',
        )
        read_only_fields = (
            'updated_date',
        )


class StarListSerializer(serializers.ModelSerializer):
    star_id = serializers.IntegerField(source='id')
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='mybook.book')

    class Meta:
        model = BookStar
        fields = (
            'star_id',
            'content',
            'updated_date',
            'book_id',
        )
