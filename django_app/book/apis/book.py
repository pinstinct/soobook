from rest_framework import generics
from rest_framework.views import APIView

from book.models import Book
from book.serializers import SearchSerializer

__all__ = (
    'Search',
    'MyBook',
)


# 주현님
class Search(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = SearchSerializer

    def get_queryset(self, **kwargs):
        # project_id may be None
        return self.queryset \
            .filter(title=self.kwargs.get('title')) \
            .filter(author=self.kwargs.get('author'))


# 성수님
class MyBook(APIView):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass
