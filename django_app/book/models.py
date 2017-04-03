from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=256)
    author = models.CharField(max_length=200)
    cover_thumbnail = models.URLField()
    publisher = models.CharField(max_length=100)
    description = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)
    google_id = models.CharField(max_length=100)
