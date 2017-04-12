from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from book.models import Book
from book.models import MyBook as MyBookModel
from book.serializer import BookSerializer, MyBookSerializer
from book.serializer.book import MyBookDetailSerializer
from book.views import search as api_search
from utils.pagination import BookPagination, MyBookPagination

__all__ = (
    'Search',
    'MyBook',
    'MyBookDetail',
    'MyBookSearch',
)
User = get_user_model()


class Search(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        field = self.request.query_params.keys()
        if field:
            keyword = self.request.query_params.get('keyword', '')
            if keyword:
                queryset = Book.objects.filter(keyword=keyword)
                count = queryset.count()
                if count < 10:
                    api_search(keyword, 1)
                return queryset
            else:
                raise exceptions.ParseError({
                    "ios_error_code": 4003,
                    "keyword": ["This field may not be blank."]
                })
        else:
            raise exceptions.ParseError({
                "ios_error_code": 4002,
                "keyword": ["This field is required."]
            })


class MyBookSearch(generics.ListAPIView):
    queryset = MyBookModel.objects.all()
    serializer_class = MyBookSerializer

    def get_queryset(self):
        # print('mybook search')
        user = self.request.user
        keyword = self.request.query_params.get('keyword', '')
        q = super().get_queryset().filter(user=user)
        if keyword != '':
            q = q.filter(book__title__contains=keyword)
        return q


class MyBookDetail(generics.ListAPIView):
    serializer_class = MyBookDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        user = self.request.user
        user_id = user.pk
        book_id = self.request.query_params.get('bookid')
        queryset = MyBookModel.objects.filter(user_id=user_id).filter(book_id=book_id)
        return queryset


class MyBook(generics.GenericAPIView):
    queryset = MyBookModel.objects.all()
    serializer_class = MyBookSerializer
    pagination_class = MyBookPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        if self.request.auth:
            user = self.request.user
            q = super().get_queryset().filter(user=user).order_by('-updated_date')

            page = self.paginate_queryset(q)
            if page is not None:
                serializer = self.get_serializer(q, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(q, many=True)
            return Response(serializer.data)
        else:
            raise exceptions.NotAuthenticated()

    def post(self, request):
        data = self.request.data.keys()
        if data:
            book_id = self.request.data.get('book_id', '')
            if book_id:
                try:
                    book = Book.objects.get(pk=book_id)
                    user = self.request.user
                    MyBookModel.objects.get_or_create(
                        user=user,
                        book=book,
                    )
                    return Response({"detail": "Successfully added."},
                                    status=status.HTTP_201_CREATED)
                except:
                    raise exceptions.ParseError({"ios_error_code": 4004, "detail": "Invalid book_id."})
            else:
                raise exceptions.ParseError({"ios_error_code": 4003, "book_id": ["This field may not be blank."]})
        else:
            raise exceptions.ParseError({"ios_error_code": 4002, "book_id": ["This field is required."]})

    def delete(self, request, *args, **kwargs):
        data = self.request.data.keys()
        if data:
            book_id = self.request.data.get('book_id', '')
            if book_id:
                try:
                    book = Book.objects.get(pk=book_id)
                    user = self.request.user
                    MyBookModel.objects.filter(user=user).filter(book=book).delete()
                    return Response({"detail": "Successfully deleted."},
                                    status=status.HTTP_200_OK)
                except:
                    raise exceptions.ParseError({"ios_error_code": 4004, "detail": "Invalid book_id."})
            else:
                raise exceptions.ParseError({"ios_error_code": 4003, "book_id": ["This field may not be blank."]})
        else:
            raise exceptions.ParseError({"ios_error_code": 4002, "book_id": ["This field is required."]})
