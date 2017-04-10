from django.conf import settings
from django.db import models

__all__ = (
    'Book',
    'MyBook',
)


class Book(models.Model):
    google_id = models.CharField(max_length=100)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=200)
    cover_thumbnail = models.URLField()
    publisher = models.CharField(max_length=100)
    description = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    keyword = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.title


class MyBook(models.Model):
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(Book)

    def __str__(self):
        return '{} : {}'.format(
            self.user,
            self.book,
        )
