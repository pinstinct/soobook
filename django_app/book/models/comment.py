from django.db import models

from book.models import MyBook


class BookComment(models.Model):
    content = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    mybook = models.ForeignKey(MyBook)

    def __str__(self):
        return self.content
