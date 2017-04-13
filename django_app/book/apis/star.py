from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import BookStar, MyBook
from book.serializer import StarSerializer

__all__ = (
    'Star',
)


class Star(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_id = request.GET["user_id"]
        book_id = request.GET["book_id"]
        mybook_id = MyBook.objects.get(user_id=user_id, book_id=book_id)

        bookstar, _ = BookStar.objects.get_or_create(mybook_id=mybook_id)
        serializer = StarSerializer(bookstar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        mybook_id = self.request.data.get('mybook_id', '')
        content = self.request.data.get('content', '')

        mybook = MyBook.objects.get(id=mybook_id)
        if mybook.user == request.user:

            bookstar, _ = BookStar.objects.get_or_create(mybook_id=mybook_id)
            bookstar.content = content
            bookstar.save()
            serializer = StarSerializer(bookstar)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
