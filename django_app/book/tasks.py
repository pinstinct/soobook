from book.models import Book
from book.views import search
from book.views.book_api import save_detail_google_book
from config.celery import app


# @app.task
# def book_google_id_data():
#     books = Book.objects.values_list('google_id', flat=True)
#     for google_id in books:
#         print(google_id)
#         save_detail_google_book(google_id)


@app.task
def book_google_id_data():
    books = Book.objects.values_list('google_id', 'publisher', 'description')
    for book in books:
        google_id = book[0]
        publisher = book[1]
        description = book[2]
        if (publisher or description) == '':
            print(google_id)
            try:
                save_detail_google_book(google_id)
            except KeyError:
                pass


@app.task
def book_keyword_data():
    books = Book.objects.values_list('keyword', flat=True)
    for keyword in books:
        search(keyword, 0, 5)
