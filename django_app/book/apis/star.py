from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from book.models import BookStar, MyBook
from book.serializer import StarSerializer
from utils.pagination import MyBookPagination

__all__ = (
    'Star',
)


class Star(generics.GenericAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = MyBookPagination

    def get(self, request):
        if self.request.auth:
            user = self.request.user
            book_list = MyBook.objects.filter(user=user)
            star_list = []
            for mybook in book_list:
                bookstar = BookStar.objects.get(mybook_id=mybook.pk)
                star_list.append(bookstar)

            page = self.paginate_queryset(star_list)
            if page is not None:
                serializer = StarSerializer(star_list, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = StarSerializer(star_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.NotAuthenticated()

    def post(self, request):
        try:
            mybook_id = self.request.data.get('mybook_id', '')
            content = self.request.data.get('content', '')
            mybook = MyBook.objects.get(id=mybook_id)
            if mybook.user == self.request.user:
                defaults = {
                    'content': content
                }
                bookstar, _ = BookStar.objects.update_or_create(
                    mybook_id=mybook_id,
                    defaults=defaults
                )
                serializer = StarSerializer(bookstar)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise exceptions.PermissionDenied()
        except (ValueError, ObjectDoesNotExist):
            raise exceptions.ParseError({"ios_error_code": 4004, "detail": "Invalid mybook_id"})
        except ValidationError:
            raise exceptions.ValidationError({"ios_error_code": 4004, "detail": "Value between 0 and 5"})
