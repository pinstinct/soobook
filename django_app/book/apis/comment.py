from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics, exceptions
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from book.models import BookComment, MyBook
from book.serializer import BookCommentSerializer

__all__ = (
    'Comment',
)


class Comment(generics.GenericAPIView):
    queryset = BookComment.objects.all()
    serializer_class = BookCommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        data = self.request.data.keys()
        try:
            mybook_id = self.request.data.get('mybook_id', '')
            content = self.request.data.get('content', '')
            mybook = MyBook.objects.get(id=mybook_id)
            if mybook.user == self.request.user:
                defaults = {
                    'content': content
                }
                q, result = super().get_queryset().update_or_create(
                    mybook_id=mybook_id,
                    defaults=defaults
                )
                if result:
                    return Response({"detail": "Successfully added."}, status=status.HTTP_201_CREATED)
                return Response({"detail": "Successfully updated."}, status=status.HTTP_200_OK)
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

    def delete(self, request):
        data = self.request.data.keys()
        try:
            comment_id = self.request.data.get('comment_id', '')
            comment = super().get_queryset().get(id=comment_id)
            user = comment.mybook.user
            if user == self.request.user:
                comment.delete()
                return Response({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
            else:
                raise exceptions.PermissionDenied()
        except ValueError:
            if data:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "comment_id": ["This field may not be blank."]})
            else:
                raise exceptions.ParseError({"ios_error_code": 4002,
                                             "comment_id": ["This field is required."]})
        except ObjectDoesNotExist:
            raise exceptions.ParseError({"ios_error_code": 4004,
                                         "detail": "Invalid comment_id"})
