from django.contrib.auth import get_user_model
from rest_framework import generics

from book.models import Book
from book.serializers import MyBookSerializer, BookSerializer
from book.views import search as api_search
from utils.pagination import BookPagination

__all__ = (
    'Search',
    'MyBook',
)
User = get_user_model()


class Search(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        queryset = Book.objects.filter(keyword=keyword)
        count = queryset.count()
        if count < 20:
            api_search(keyword)
        return queryset


class MyBook(generics.CreateAPIView):
    serializer_class = MyBookSerializer
