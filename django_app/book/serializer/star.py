from rest_framework import serializers

from book.models import BookStarRating


class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookStarRating
        fields = (
            'content',
            'created_date',
            'user',
            'book',
        )
