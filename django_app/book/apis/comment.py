from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response

from book.models import MyBook as MyBookModel
from book.serializer import CommentSerializer
from utils.pagination import CommentPagenation

__all__ = (
    'Comment',

)

User = get_user_model()


class Comment(generics.GenericAPIView,
              mixins.ListModelMixin,
              mixins.DestroyModelMixin,
              mixins.UpdateModelMixin):
    serializer_class = CommentSerializer
    pagination_class = CommentPagenation
    queryset = MyBookModel.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        permission = self.request.auth
        if permission:
            field = self.request.data.keys()
            if field:
                book_id = self.request.data.get('book_id', '')
                if book_id:
                    book = MyBookModel.object.get(pk=book_id)
                    if book:
                        try:
                            user = self.request.user
                            user_id = user.pk
                            content = self.request.data.get('content','')
                            comment, _ = Comment.objects.get_or_create(book_id=book_id , user_id=user_id)
                            Comment.content = content
                            comment.save()
                            serializer = CommentSerializer(comment)
                            return Response(serializer.data, {
                                "detail": "Successfully Comment added."
                            }, status=status.HTTP_201_CREATED)
                        except:
                            raise exceptions.ParseError({
                                "ios_error_code": 1,
                                "content": ["Null values are not allowed in this field"]
                            })

                else:
                    raise exceptions.ParseError({
                        "ios_error_code": 4003,
                        "book_id": ["This field may not be blank."]
                    })
            else:
                raise exceptions.ParseError({
                    "ios_error_code": 4002,
                    "book_id": ["This field is required."]
                })
        else:
            raise exceptions.AuthenticationFailed()

    def delete(self, request, *args, **kwargs):
        permission = self.request.auth
        if permission:
            field = self.request.data.keys()
            if field:
                book_id = self.request.data.get('book_id', '')
                if book_id:
                    comment_id = Comment.object.get('comment_id', '')
                    if comment_id:
                        try:
                            user = self.request.user
                            user_id = user.pk
                            Comment.objects.filter(user_id=user_id).filter(book_id=book_id).filter(comment_id=comment_id).delete()
                            return Response({
                                "detail": "Successfully Comment deleted."}, status=status.HTTP_201_OK)
                        except:
                            raise exceptions.ParseError({
                                "ios_error_code": 1,
                                "comment": ["field delete"]
                            })


                else:
                    raise exceptions.ParseError({
                        "ios_error_code": 4003,
                        "book_id": ["This field may not be blank."]
                    })
            else:
                raise exceptions.ParseError({
                    "ios_error_code": 4002,
                    "book_id": ["This field is required."]
                })
        else:
            raise exceptions.AuthenticationFailed()

    def put(self, request, *args, **kwargs):
        permission = self.request.auth
        if permission:
            field = self.request.data.keys()
            if field:
                book_id = self.request.data.get('book_id', '')
                if book_id:
                    comment_id = Comment.object.get('comment_id', '')
                    if comment_id:
                        try:
                            user = self.request.user
                            user_id = user.pk
                            content = self.request.data.get('content', '')
                            Comment.objects.filter(user_id=user_id).filter(book_id=book_id).filter(comment_id=comment_id).update(content)
                            return Response({
                                "detail": "Successfully update." }, status=status.HTTP_201_OK)
                        except:
                            raise exceptions.ParseError({
                                "ios_error_code": 5000,
                                "comment": ["filed update"]
                            })

                else:
                    raise exceptions.ParseError({
                        "ios_error_code": 4003,
                        "book_id": ["This field may not be blank."]
                    })
            else:
                raise exceptions.ParseError({
                    "ios_error_code": 4002,
                    "book_id": ["This field is required."]
                })
        else:
            raise exceptions.AuthenticationFailed()