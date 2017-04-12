from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import BookStar
from book.serializer import StarSerializer

__all__ = (
    'Star',
)


class Star(APIView):
    def get(self, request):
        mybook_id = request.GET["mybook_id"]
        bookstar, _ = BookStar.objects.get_or_create(mybook_id=mybook_id)
        serializer = StarSerializer(bookstar)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # mybook_id = request.POST["mybook_id"]
        # content = request.POST["content"]
        # bookstar, _ = BookStar.objects.get_or_create(mybook_id=mybook_id)
        # bookstar.content = content
        # bookstar.save()
        # serializer = StarSerializer(bookstar)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = StarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

