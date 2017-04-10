from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from book.models import MyBook


class BookStarRating(models.Model):
    content = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_date = models.DateTimeField(auto_now=True)
    mybook = models.ForeignKey(MyBook)

    def __str__(self):
        return '{} : {} : {}'.format(
            self.user,
            self.book,
            self.content,
        )
