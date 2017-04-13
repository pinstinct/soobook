from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from book.models import MyBook
from config import settings

__all__ = (
    'BookStar',
)


class BookStar(models.Model):
    content = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_date = models.DateTimeField(auto_now=True)
    mybook = models.ForeignKey(MyBook)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __str__(self):
        return '{} : {} : {}'.format(
            self.mybook.user,
            self.mybook.book,
            self.content,
        )

    def get_formated_star(self):
        star = int(self.content)
        return star / 2 if star > 0 else 0
