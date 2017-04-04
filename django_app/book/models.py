from django.db import models


# User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=200)
    cover_thumbnail = models.URLField()
    publisher = models.CharField(max_length=100)
    description = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    google_id = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# class MyBookShelf(models.Model):
#     my_book = models.ForeignKey(Book)
#     user = models.ForeignKey(User)
#     created_date = models.DateTimeField(auto_now_add=True)
