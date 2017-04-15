from rest_framework import serializers

from book.models import BookStar

__all__ = (
    'StarSerializer',
)


class StarSerializer(serializers.ModelSerializer):
    star_id = serializers.IntegerField(source='id')

    class Meta:
        model = BookStar
        fields = (
            'star_id',
            'rating',
            'created_date',
        )
        read_only_fields = (
            'created_date',
        )
