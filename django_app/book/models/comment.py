from django.conf import settings
from django.db import models

from book.models import MyBook

__all__ = (
    'Comment',
)


class Comment(models.Model):
    updated_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(MyBook)
    comment = models.TextField(max_length=2000)

    def __str__(self):
        return '{} : {}'.format(
            self.updated_date,
            self.book,
            self.comment,
        )
