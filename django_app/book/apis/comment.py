from rest_framework import generics
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
        comment = self.request.data.get('comment')
        defaults = {
            'comment': comment
        }
        q, _ = BookComment.objects.update_or_create(
            mybook_id=mybook_id,
            defaults=defaults
        )

        serializer = self.get_serializer(q)
        return Response(serializer.data)
