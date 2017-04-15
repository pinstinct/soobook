from rest_framework import generics, exceptions
from rest_framework import status
from rest_framework.response import Response

from book.models import BookComment, MyBook
from book.serializer import BookCommentSerializer

__all__ = (
    'Comment',
)


class Comment(generics.GenericAPIView, ):
    queryset = BookComment.objects.all()
    serializer_class = BookCommentSerializer
    permission_classes = ()

    def get(self, request):
        if request.auth:
            user_id = request.GET["user_id"]
            if user_id:
                book_list = MyBook.objects.filter(user_id=user_id)
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
        if request.auth:
            mybook_id = self.request.data.get('mybook_id')
            comment = self.request.data.get('comment')
            mybook = MyBook.objects.get(id=mybook_id)
            if mybook.user == request.user:

                defaults = {
                    'comment': comment
                }
                q, _ = BookComment.objects.update_or_create(
                    mybook_id=mybook_id,
                    defaults=defaults
                )

                serializer = self.get_serializer(q)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                raise exceptions.ParseError({"detail": "This is not an account on this soobook"})
        else:
            raise exceptions.NotAuthenticated()

    def delete(self, request):
        if request.auth:
            comment_id = self.request.data.get('comment_id')
            if comment_id:
                q = super().get_queryset().get(id=comment_id)
                if q:
                    q.delete()
                    return Response({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
            else:
                raise exceptions.ParseError({"detail": "This is a nonexistent comment"})
        else:
            raise exceptions.NotAuthenticated()
