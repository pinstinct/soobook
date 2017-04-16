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

    def get(self, request):
        if self.request.auth:
            user = self.request.user
            if user:
                book_list = MyBook.objects.filter(user_id=user)
                comment_list = []
                for mybook in book_list:
                    comment, _ = BookComment.objects.get_or_create(mybook_id=mybook.pk)
                    comment_list.append(comment)
                serializer = BookCommentSerializer(comment_list, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise exceptions.ParseError({"ios_error_code": 4003, "detail": "Invalid user_id"})
        else:
            raise exceptions.NotAuthenticated()

    def post(self, request):
        mybook_id = self.request.data.get('mybook_id')
        content = self.request.data.get('content')
        mybook = MyBook.objects.get(id=mybook_id)
        if mybook.user == request.user:
            defaults = {
                'content': content
            }
            q, _ = BookComment.objects.update_or_create(
                mybook_id=mybook_id,
                defaults=defaults
            )
            serializer = self.get_serializer(q)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise exceptions.PermissionDenied()

    def delete(self, request):
        comment_id = self.request.data.get('comment_id')
        if comment_id:
            q = super().get_queryset().get(id=comment_id)
            if q:
                q.delete()
                return Response({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
        else:
            raise exceptions.ParseError({"ios_error_code": 4004, "detail": "Invalid comment_id."})
