from rest_framework import serializers

from book.models import BookComment

__all__ = (
    'BookCommentSerializer',
)


class BookCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookComment
        fields = (
            'id',
            'content',
            'updated_date',
        )
