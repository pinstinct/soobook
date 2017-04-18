from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings

from book.models import BookMark
from book.models import MyBook
from book.serializer.mark import BookMarkSerializer

__all__ = (
    'Mark',
)


class Mark(generics.GenericAPIView):
    queryset = BookMark.objects.all()
    serializer_class = BookMarkSerializer

    def post(self, request):
        # user = self.request.user
        mybook_id = self.request.data.get('mybook_id')
        content = self.request.data.get('content')

        # try:
        # mybook = MyBook.objects.filter(user=user).filter(book=book).get()
        mybook = MyBook.objects.get(id=mybook_id)
        q, _ = BookMark.objects.get_or_create(
            mybook=mybook,
            content=content,
        )

        serializer = self.get_serializer(q)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except:
        #     # book.models.book.DoesNotExist: MyBookmatching query does not exist.
        #     pass

    def soobook_exception(self, data):
        try:
            return {'Location': data[api_settings.URL_FIELD_NAME]}
        except (TypeError, KeyError):
            return {}

    def put(self, request):
        bookmakr_id = self.request.data.get('mark_id')
        content = self.request.data.get('content')
        q = super().get_queryset().filter(id=bookmakr_id).get()
        q.content = content
        q.save()
        serializer = self.get_serializer(q)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        bookmark_id = self.request.data.get('mark_id')
        q = super().get_queryset().filter(id=bookmark_id).get()
        q.delete()
        serializer = self.get_serializer(q)
        return Response(serializer.data, status=status.HTTP_200_OK)
