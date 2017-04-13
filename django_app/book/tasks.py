from book.models import Book
from book.views import search
from book.views.book_api import save_detail_google_book
from config.celery import app


@app.task
def book_google_id_data():
    books = Book.objects.values_list('google_id', 'publisher', 'description', 'cover_thumbnail')
    for book in books:
        google_id = book[0]
        publisher = book[1]
        description = book[2]
        cover_thumbnail = book[3]
        if publisher == '' or description == '' or cover_thumbnail == '':
            try:
                save_detail_google_book(google_id)
            except KeyError:
                pass


@app.task
def book_keyword_data():
    books = Book.objects.values_list('keyword', flat=True)
    for keyword in books:
        count = Book.objects.filter(keyword=keyword).count()
        if count < 50:
            try:
                search(keyword, 0, 5)
            except KeyError:
                pass
