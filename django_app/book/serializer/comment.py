from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.models import Comment

__all__ = (
    'CommentSerializer',
)

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        field = (
            'id',
            'book_id',
            'created_date',
            'comment_id',
            'content',

        )

        read_only_fields = (
            'created_date',
        )
