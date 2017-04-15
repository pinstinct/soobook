from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from book.models import BookComment
from book.serializer import BookCommentSerializer

__all__ = (
    'Comment',
)


class Comment(generics.GenericAPIView):
    queryset = BookComment.objects.all()
    serializer_class = BookCommentSerializer

    def post(self, request):
        mybook_id = self.request.data.get('mybook_id')
        content = self.request.data.get('content')
        defaults = {
            'content': content
        }
        q, _ = BookComment.objects.update_or_create(
            mybook_id=mybook_id,
            defaults=defaults
        )

        serializer = self.get_serializer(q)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        comment_id = self.request.data.get('comment_id')
        q = super().get_queryset().get(id=comment_id)
        if q:
            q.delete()
            return Response({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
