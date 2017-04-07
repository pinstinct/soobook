# 주현님









# 성수님

from rest_framework import serializers

from book.models import Book


class MyBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = (
            'title',
            'author',
            'cover_thumbnail',
            'publisher',
            'description',
        )
