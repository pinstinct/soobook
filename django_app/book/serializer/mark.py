from rest_framework import serializers

from book.models import BookMark

__all__ = (
    'BookMarkSerializer',
)


class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = (
            'id',
            'content',
            'update_date',
        )
