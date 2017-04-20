from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from book.models import Book, BookStar
from book.models import MyBook as MyBookModel
from book.serializer import MyBookSerializer, BookSerializer, MyBookDetailSerializer
from book.views.book_api import search_data
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
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('title', 'author', 'keyword', 'publisher')
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title', 'author', 'keyword', 'publisher')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        keyword = kwargs.get('keyword')

        if count < 10:
            search_data(keyword, 0, 2)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        data = self.request.query_params.keys()
        if data:
            keyword = self.request.query_params.get('keyword', '')
            if keyword != '':
                return self.list(request, keyword=keyword)
            else:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "keyword": ["This field may not be blank."]})
        else:
            raise exceptions.ParseError({"ios_error_code": 4002,
                                         "keyword": ["This field is required."]})


class MyBookSearch(generics.ListAPIView):
    queryset = MyBookModel.objects.all()
    serializer_class = MyBookSerializer
    pagination_class = MyBookPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        data = self.request.query_params.keys()
        if data:
            user = self.request.user
            keyword = self.request.query_params.get('keyword', '')
            q = super().get_queryset().filter(user=user)
            if keyword != '':
                q = q.filter(book__title__contains=keyword)
                return q
            else:
                raise exceptions.ParseError({"ios_error_code": 4003, "keyword": ["This field may not be blank."]})
        else:
            raise exceptions.ParseError({"ios_error_code": 4002, "keyword": ["This field is required."]})

    def get(self, request, *args, **kwargs):
        if self.request.auth:
            self.get_queryset()
        else:
            raise exceptions.NotAuthenticated()
        return self.list(self, request)


class MyBookDetail(generics.GenericAPIView):
    queryset = MyBookModel.objects.all()
    serializer_class = MyBookDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        if self.request.auth:
            data = self.request.query_params.keys()
            try:
                book_id = self.request.query_params.get('bookid', '')
                book = Book.objects.get(pk=book_id)
                user = self.request.user
                q = super().get_queryset().filter(user=user).filter(book=book)
                serializer = self.get_serializer(q, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                if data:
                    raise exceptions.ParseError({"ios_error_code": 4003,
                                                 "bookid": ["This field may not be blank."]})
                else:
                    raise exceptions.ParseError({"ios_error_code": 4002,
                                                 "bookid": ["This field is required."]})
            except ObjectDoesNotExist:
                raise exceptions.ParseError({"ios_error_code": 4004,
                                             "detail": "Invalid bookid"})
        else:
            raise exceptions.NotAuthenticated()


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
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotAuthenticated()

    def post(self, request):
        data = self.request.data.keys()
        try:
            book_id = self.request.data.get('book_id', '')
            book = Book.objects.get(pk=book_id)
            user = self.request.user

            mybook, result = super().get_queryset().get_or_create(user=user, book=book)
            BookStar.objects.update_or_create(mybook=mybook)

            if result:
                return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"detail": "Already added."}, status=status.HTTP_200_OK)
        except ValueError:
            if data:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "book_id": ["This field may not be blank."]})
            else:
                raise exceptions.ParseError({"ios_error_code": 4002,
                                             "book_id": ["This field is required."]})
        except ObjectDoesNotExist:
            raise exceptions.ParseError({"ios_error_code": 4004,
                                         "detail": "Invalid book_id"})

    def delete(self, request):
        data = self.request.data.keys()
        try:
            book_id = self.request.data.get('book_id', '')
            book = Book.objects.get(pk=book_id)
            user = self.request.user

            q = super().get_queryset().filter(user=user).filter(book=book)
            q.delete()
            return Response({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
        except ValueError:
            if data:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "book_id": ["This field may not be blank."]})
            else:
                raise exceptions.ParseError({"ios_error_code": 4002,
                                             "book_id": ["This field is required."]})
        except ObjectDoesNotExist:
            raise exceptions.ParseError({"ios_error_code": 4004,
                                         "detail": "Invalid book_id"})
