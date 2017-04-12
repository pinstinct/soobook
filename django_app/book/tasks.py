from book.models import Book
from book.views import search
from config.celery import app


@app.task
def book_data():
    keyword_list = Book.objects.values_list('keyword', flat=True)
    for keyword in keyword_list:
        print(keyword)
    search(keyword, 1)
