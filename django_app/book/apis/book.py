from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response

from book.models import Book
from book.serializers import BookSerializer
from book.serializers import MyBookSerializer
from book.views import search as api_search
from utils.pagination import BookPagination, MyBookPagination

__all__ = (
    'Search',
    'MyBook',
)
User = get_user_model()


class Search(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        field = self.request.query_params.keys()
        if field:
            print(field)
            keyword = self.request.query_params.get('keyword', '')
            print(keyword)
            if keyword:
                queryset = Book.objects.filter(keyword=keyword)
                count = queryset.count()
                if count < 20:
                    api_search(keyword)
                return queryset
            else:
                raise exceptions.ParseError({
                    "ios_error_code": 4003,
                    "book_id": ["This field may not be blank."]
                })
        else:
            raise exceptions.ParseError({
                "ios_error_code": 4002,
                "keyword": ["This field is required."]
            })


class MyBook(generics.GenericAPIView,
             mixins.ListModelMixin,
             mixins.DestroyModelMixin):
    serializer_class = MyBookSerializer
    pagination_class = MyBookPagination

    def get_queryset(self):
        field = self.request.query_params.keys()
        if field:
            user_id = self.request.query_params.get('userid', None)
            if user_id:
                queryset = Book.objects.filter(myuser=user_id)
                return queryset
            else:
                raise exceptions.ParseError({
                    "ios_error_code": 4003,
                    "userid": ["This field may not be blank."]
                })
        else:
            raise exceptions.ParseError({
                "ios_error_code": 4002,
                "userid": ["This field is required."]
            })

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        permission = self.request.auth
        if permission:
            param = self.request.data.keys()
            if param:
                book_id = self.request.data.get('book_id', '')
                if book_id:
                    try:
                        book = Book.objects.get(pk=book_id)
                    except:
                        raise exceptions.ParseError({
                            "ios_error_code": 4004,
                            "detail": "Invalid book_id."
                        })
                    self.request.user.mybook.add(book)
                    serializer = MyBookSerializer(book)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    raise exceptions.ParseError({
                        "ios_error_code": 4003,
                        "book_id": ["This field may not be blank."]
                    })
            else:
                raise exceptions.ParseError({
                    "ios_error_code": 4002,
                    "book_id": ["This field is required."]
                })
        else:
            raise exceptions.AuthenticationFailed()

    def delete(self, request, *args, **kwargs):
        permission = self.request.auth
        if permission:
            param = self.request.data.keys()
            if param:
                book_id = self.request.data.get('book_id', '')
                if book_id:
                    try:
                        book = Book.objects.get(pk=book_id)
                    except:
                        raise exceptions.ParseError({
                            "ios_error_code": 4004,
                            "detail": "Invalid book_id."
                        })
                    self.request.user.mybook.remove(book)
                    return Response({
                        "detail": "Successfully deleted."
                    }, status=status.HTTP_200_OK)
                else:
                    raise exceptions.ParseError({
                        "ios_error_code": 4003,
                        "book_id": ["This field may not be blank."]
                    })
            else:
                raise exceptions.ParseError({
                    "ios_error_code": 4002,
                    "book_id": ["This field is required."]
                })
        else:
            raise exceptions.AuthenticationFailed()
