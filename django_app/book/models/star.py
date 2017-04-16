from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from book.models import MyBook

__all__ = (
    'BookStar',
)


class BookStar(models.Model):
    content = models.FloatField(
        default=0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(5)]
    )
    updated_date = models.DateTimeField(auto_now=True)
    mybook = models.ForeignKey(MyBook)

    def __str__(self):
        return '{} : {} : {}'.format(
            self.mybook.user,
            self.mybook.book,
            self.rating,
        )

    def get_formated_star(self):
        star = int(self.rating)
        return star / 2 if star > 0 else 0
