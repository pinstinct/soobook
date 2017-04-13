from rest_framework import serializers

from book.models import BookStar

__all__ = (
    'StarSerializer',
)


class StarSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookStar
        fields = (
            'content',
            'created_date',
            'mybook',
        )
        read_only_fields = (
            'created_date',
        )
