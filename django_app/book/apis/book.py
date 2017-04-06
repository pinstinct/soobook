from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import SearchSerializer

__all__ = (
    'Search',
    'MyBook',
)


# 주현님
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 1000


class Search(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Book.objects.all()
    serializer_class = SearchSerializer
    pagination_class = StandardResultsSetPagination

    # @csrf_exempt
    def list(self, request):
        keyword = request.GET['keyword']
        books = self.queryset.filter(keyword=keyword)
        serializer = SearchSerializer(books, many=True)
        return Response(serializer.data)


class MyBook(APIView):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass
