from django.conf import settings
from django.db import models

from book.models import MyBook

__all__ = (
    'Comment',
)


class Comment(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    mybook = models.ForeignKey(MyBook)
    content = models.TextField(max_length=2000, null=False)
    comment_id = models.CharField(max_length=100)

    def __str__(self):
        return '{} : {} : {}'.format(
            self.created_date,
            self.book,
            self.content,
        )
