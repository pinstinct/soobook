from django.db import models

from book.models import MyBook


class BookComment(models.Model):
    comment = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    mybook = models.ForeignKey(MyBook)
