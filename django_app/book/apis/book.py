from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import MyBookSerializer

__all__ = (
    'Search',
    'MyBook',
)

User = get_user_model()


# 주현님
class Search(APIView):
    def get(self):
        pass


# 성수님
class MyBook(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):
        user_pk = request.GET["user_pk"]
        mybook = Book.objects.filter(myuser=user_pk)
        serializer = MyBookSerializer(mybook, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            book_pk = request.data["book_pk"]
            book = Book.objects.get(pk=book_pk)
            request.user.mybook.add(book)
            serializer = MyBookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except (AttributeError, ObjectDoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            book_pk = request.data["book_pk"]
            book = Book.objects.get(pk=book_pk)
            request.user.mybook.remove(book)
            return Response(status=status.HTTP_200_OK)
        except MultiValueDictKeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except (AttributeError, ObjectDoesNotExist):
            return Response(status=status.HTTP_400_BAD_REQUEST)