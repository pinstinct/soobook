from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import BookSerializer
from book.serializers import MyBookSerializer
from book.views import search as api_search
from utils.pagination import BookPagination

__all__ = (
    'Search',
    # 'SearchFix',
    'MyBook',
)
User = get_user_model()


class Search(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', None)
        if keyword is not None:
            queryset = Book.objects.filter(keyword=keyword)
            count = queryset.count()
            if count < 20:
                api_search(keyword)
            return queryset
        else:
            raise exceptions.ParseError({"ios_error_code": 4001, "keyword": ["This field is required."]})


class MyBook(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        user_pk = request.GET["userid"]
        mybook = Book.objects.filter(myuser=user_pk)
        serializer = MyBookSerializer(mybook, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            book_pk = request.data["book_id"]
            book = Book.objects.get(pk=book_pk)
            request.user.mybook.add(book)
            serializer = MyBookSerializer(book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except (AttributeError, ObjectDoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            book_pk = request.data["book_id"]
            book = Book.objects.get(pk=book_pk)
            request.user.mybook.remove(book)
            return Response(status=status.HTTP_200_OK)
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except (AttributeError, ObjectDoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)
