from django.db import models

from book.models import MyBook


class BookMark(models.Model):
    content = models.TextField()
    update_date = models.DateTimeField(auto_now=True)
    mybook = models.ForeignKey(MyBook)

    def __str__(self):
        return self.content
