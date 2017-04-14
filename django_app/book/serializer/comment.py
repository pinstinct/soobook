from rest_framework import serializers

from book.models import BookComment

__all__ = (
    'BookCommentSerializer',
)


class BookCommentSerializer(serializers.ModelSerializer):
    comment_id = serializers.IntegerField(source='id')

    class Meta:
        model = BookComment
        fields = (
            'comment_id',
            'comment',
            'updated_date',
        )
