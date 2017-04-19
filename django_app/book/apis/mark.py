from django.core.exceptions import ObjectDoesNotExist
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from book.models import BookMark
from book.models import MyBook
from book.serializer.mark import BookMarkSerializer

__all__ = (
    'Mark',
)


class Mark(generics.GenericAPIView):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        data = self.request.data.keys()
        try:
            mybook_id = self.request.data.get('mybook_id', '')
            content = self.request.data.get('content', '')
            mybook = MyBook.objects.get(pk=mybook_id)
            if mybook.user == self.request.user:
                q, result = super().get_queryset().get_or_create(
                    mybook=mybook,
                    content=content,
                )
                if result:
                    return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"detail": "Already added."}, status=status.HTTP_200_OK)
            else:
                raise exceptions.PermissionDenied()
        except ValueError:
            if data:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "detail": ["'mybook_id', 'content' field may not be blank."]})
            else:
                raise exceptions.ParseError({"ios_error_code": 4002,
                                             "detail": ["'mybook_id', 'content' field is required."]})
        except ObjectDoesNotExist:
            raise exceptions.ParseError({"ios_error_code": 4004,
                                         "detail": "Invalid mybook_id"})

    def put(self, request):
        data = self.request.data.keys()
        try:
            bookmark_id = self.request.data.get('mark_id', '')
            content = self.request.data.get('content', '')
            mark = super().get_queryset().get(pk=bookmark_id)
            user = mark.mybook.user
            if user == self.request.user:
                mark.content = content
                mark.save()
                return Response({"detail": "Successfully updated."}, status=status.HTTP_200_OK)
            else:
                raise exceptions.PermissionDenied()
        except ValueError:
            if data:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "detail": ["'mark_id', 'content' field may not be blank."]})
            else:
                raise exceptions.ParseError({"ios_error_code": 4002,
                                             "detail": ["'mark_id', 'content' field is required."]})
        except ObjectDoesNotExist:
            raise exceptions.ParseError({"ios_error_code": 4004,
                                         "detail": "Invalid mark_id"})

    def delete(self, request):
        data = self.request.data.keys()
        try:
            bookmark_id = self.request.data.get('mark_id', '')
            mark = super().get_queryset().get(pk=bookmark_id)
            user = mark.mybook.user
            if user == self.request.user:
                mark.delete()
                return Response({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
            else:
                raise exceptions.PermissionDenied()
        except ValueError:
            if data:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "mark_id": ["This field may not be blank."]})
            else:
                raise exceptions.ParseError({"ios_error_code": 4002,
                                             "mark_id": ["This field is required."]})
        except ObjectDoesNotExist:
            raise exceptions.ParseError({"ios_error_code": 4004,
                                         "detail": "Invalid mark_id"})
