from rest_framework import serializers

from book.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        field = (
            'updated_date',
            'book',
            'comment',
        )
