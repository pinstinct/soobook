from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework import status
from rest_framework.filters import SearchFilter
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
    filter_backends = (SearchFilter,)
    search_fields = ('title', 'author', 'keyword', 'publisher')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.count()
        keyword = kwargs.get('keyword')

        if count < 10:
            try:
                search_data(keyword, 0, 2)
            except KeyError:
                raise exceptions.NotFound()

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
    filter_backends = (SearchFilter,)
    search_fields = ('book__title', 'book__author', 'book__publisher')

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if self.request.auth:
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
        else:
            raise exceptions.NotAuthenticated()


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


class HasUserIdInParamsOrIsAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print('has_object_permission')
        print(request.user.is_authenticated())
        if ('user_id' in request.query_params or request.user.is_authenticated()) \
                and request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user


class MyBook(generics.GenericAPIView,
             mixins.ListModelMixin,
             mixins.CreateModelMixin,
             mixins.DestroyModelMixin):
    queryset = MyBookModel.objects.all()
    serializer_class = MyBookSerializer
    pagination_class = MyBookPagination
    permission_classes = (
        # IsAuthenticated,
        HasUserIdInParamsOrIsAuthenticated,
    )

    def get_queryset(self):
        if self.request.user.is_authenticated():
            return MyBookModel.objects.filter(user=self.request.user).order_by('-updated_date')
        else:
            raise exceptions.NotAuthenticated()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
