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
    serializer_class = BookSerializer
    pagination_class = BookPagination

    def get_queryset(self):
        field = self.request.query_params.keys()
        if field:
            keyword = self.request.query_params.get('keyword', '')
            if keyword:
                queryset = Book.objects.filter(keyword=keyword)
                count = queryset.count()
                if count < 20:
                    api_search(keyword)
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
        print('mybook search')
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
    serializer_class = MyBookSerializer
    pagination_class = MyBookPagination
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        user = self.request.user
        user_id = user.pk
        queryset = MyBookModel.objects.filter(user_id=user_id).order_by('-updated_date')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = self.request.user
        user_id = user.pk
        book_id = self.request.data.get('book_id')
        MyBookModel.objects.get_or_create(
            user_id=user_id,
            book_id=book_id,
        )
        return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)

    # def post(self, request):
    #     permission = self.request.auth
    #     if permission:
    #         # field = self.request.data.keys()
    #         # if field:
    #         try:
    #             book_id = self.request.data.get('book_id', '')
    #             if book_id:
    #                 try:
    #                     book = Book.objects.get(pk=book_id)
    #                 except:
    #                     raise exceptions.ParseError({
    #                         "ios_error_code": 4004,
    #                         "detail": "Invalid book_id."
    #                     })
    #                 user = self.request.user
    #                 user_id = user.pk
    #                 MyBookModel.objects.get_or_create(
    #                     user_id=user_id,
    #                     book_id=book_id,
    #                 )
    #
    #                 # self.request.user.mybook_set.add(book)
    #                 return Response({
    #                     "detail": "Successfully added."
    #                 }, status=status.HTTP_201_CREATED)
    #             else:
    #                 raise exceptions.ParseError({
    #                     "ios_error_code": 4003,
    #                     "book_id": ["This field may not be blank."]
    #                 })
    #         except:
    #             raise exceptions.ParseError({
    #                 "ios_error_code": 4002,
    #                 "book_id": ["This field is required."]
    #             })
    #     else:
    #         raise exceptions.AuthenticationFailed()

    def delete(self, request, *args, **kwargs):
        permission = self.request.auth
        if permission:
            field = self.request.data.keys()
            if field:
                book_id = self.request.data.get('book_id', '')
                if book_id:
                    try:
                        book = Book.objects.get(pk=book_id)
                    except:
                        raise exceptions.ParseError({
                            "ios_error_code": 4004,
                            "detail": "Invalid book_id."
                        })
                    user = self.request.user
                    user_id = user.pk
                    MyBookModel.objects.filter(user_id=user_id).filter(book_id=book_id).delete()
                    # self.request.user.mybook.remove(book)
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
