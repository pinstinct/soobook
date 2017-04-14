from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import ValidationError
from rest_framework import exceptions
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import BookStar, MyBook
from book.serializer import StarSerializer

__all__ = (
    'Star',
)


class Star(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request):

        user_id = request.GET["user_id"]
        if user_id:
            book_list = MyBook.objects.filter(user_id=user_id)
            star_list = []
            for mybook in book_list:
                bookstar, _ = BookStar.objects.get_or_create(mybook_id=mybook.pk)
                star_list.append(bookstar)
            serializer = StarSerializer(star_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.ParseError({"ios_error_code": 4003, "detail": "Invalid user_id"})

    def post(self, request):

        mybook_id = self.request.data.get('mybook_id', '')
        content = self.request.data.get('content', '')

        try:
            mybook = MyBook.objects.get(id=mybook_id)
            if mybook.user == request.user:

                bookstar, _ = BookStar.objects.get_or_create(mybook_id=mybook_id)
                bookstar.content = content
                bookstar.full_clean()
                bookstar.save()
                serializer = StarSerializer(bookstar)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise exceptions.NotAuthenticated()
        except (ValueError, ObjectDoesNotExist):
            raise exceptions.ParseError({"ios_error_code": 4004, "detail": "Invalid mybook_id"})
        except ValidationError:
            raise exceptions.ValidationError({"ios_error_code": 4004, "detail": "Value between 1 and 10"})
