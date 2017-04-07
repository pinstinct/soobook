from django.db import models


class Book(models.Model):
    google_id = models.CharField(max_length=100)
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=200)
    cover_thumbnail = models.URLField()
    publisher = models.CharField(max_length=100)
    description = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    keyword = models.CharField(max_length=200)

    def __str__(self):
        return self.title
