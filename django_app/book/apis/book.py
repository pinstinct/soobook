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
    template_name = 'book/index.html'

    def get_search_result_query(self, **kwargs):
        # project_id may be None
        return self.queryset.filter(keyword=self.kwargs.get('keyword'))

class MyBook(APIView):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass
