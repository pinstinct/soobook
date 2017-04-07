# 주현님









# 성수님

from rest_framework import serializers

from book.models import Book
from member.models import MyUser


class MyBookSerializer(serializers.ModelSerializer):
    mybook = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), write_only=True)

    class Meta:
        model = Book
        fields = (
            'mybook',
            'title',
            'author',
            'cover_thumbnail',
            'publisher',
            'description',
        )
