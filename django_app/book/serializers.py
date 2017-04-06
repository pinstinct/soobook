# 주현님
from rest_framework import serializers

from book.models import Book


class SearchSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    author = serializers.CharField(max_length=200)
    cover_thumbnail = serializers.URLField()
    publisher = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=1000)
    keyword = serializers.CharField(max_length=200)

    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'cover_thumbnail',
            'publisher',
            'description',
            'keyword'
        ]













        # 성수님
