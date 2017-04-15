from rest_framework import serializers

from book.models import BookStar

__all__ = (
    'StarSerializer',
)


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStar
        fields = (
            'id',
            'content',
            'created_date',
        )
        read_only_fields = (
            'created_date',
        )
