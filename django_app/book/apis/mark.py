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
        if data:
            mybook_id = self.request.data.get('mybook_id', '')
            content = self.request.data.get('content', '')
            if mybook_id and content != '':
                try:
                    mybook = MyBook.objects.get(id=mybook_id)
                    q, _ = BookMark.objects.get_or_create(
                        mybook=mybook,
                        content=content,
                    )
                    serializer = self.get_serializer(q)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except:
                    raise exceptions.ParseError({"ios_error_code": 4004, "detail": "Invalid mybook_id."})
            else:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "detail": ["'mybook_id', 'content' field may not be blank."]})
        else:
            raise exceptions.ParseError({"ios_error_code": 4002,
                                         "detail": ["'mybook_id', 'content' field is required."]})

    def put(self, request):
        data = self.request.data.keys()
        if data:
            bookmakr_id = self.request.data.get('mark_id', '')
            content = self.request.data.get('content', '')
            if bookmakr_id and content != '':
                try:
                    q = super().get_queryset().filter(id=bookmakr_id).get()
                    q.content = content
                    q.save()
                    serializer = self.get_serializer(q)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except:
                    raise exceptions.ParseError({"ios_error_code": 4004, "detail": "Invalid mark_id."})
            else:
                raise exceptions.ParseError({"ios_error_code": 4003,
                                             "detail": ["'mark_id', 'content' field may not be blank."]})
        else:
            raise exceptions.ParseError({"ios_error_code": 4002,
                                         "detail": ["'mark_id', 'content' field is required."]})

    def delete(self, request):
        data = self.request.data.keys()
        if data:
            bookmark_id = self.request.data.get('mark_id', '')
            if bookmark_id != '':
                try:
                    q = super().get_queryset().filter(id=bookmark_id).get()
                    q.delete()

                    return Response({"detail": "Successfully deleted."}, status=status.HTTP_200_OK)
                except:
                    raise exceptions.ParseError({"ios_error_code": 4004, "detail": "Invalid mark_id."})
            else:
                raise exceptions.ParseError({"ios_error_code": 4003, "mark_id": ["This field may not be blank."]})
        else:
            raise exceptions.ParseError({"ios_error_code": 4002, "mark_id": ["This field is required."]})
