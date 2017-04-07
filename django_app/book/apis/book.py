from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import mixins
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

    def get(self, request, user_id):
        mybook = Book.objects.filter(myuser=user_id)
        serializer = MyBookSerializer(mybook, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.user.pk)
        serializer = MyBookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        mybook = Book.objects.filter(myuser=request.user.pk)
        mybook.delete()
        return Response(status=status.HTTP_200_OK)

