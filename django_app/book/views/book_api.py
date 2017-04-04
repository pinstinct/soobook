import requests
from django.shortcuts import render

from book.models import Book
from config.settings import config

__all__ = (
    'search_from_google_books',
    'search',
)


def search_from_google_books(keyword, index=0):
    if index:
        index = index
    else:
        index = 10
    print(index)
    params = {
        'q': keyword,
        'langRestrict': 'ko',
        'maxResults': 10,
        'startIndex': index,
        'orderBy': 'relevance',
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
    result_dic = r.json()

    return result_dic


def get_isbn_from_google_book(google_id):
    params = {
        'volumeId': google_id
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes/volumeId', params=params)
    result_dict = r.json()
    identifiers = result_dict['volumeInfo']['industryIdentifiers']
    for identifier in identifiers:
        if identifier['type'] == 'ISBN_13':
            isbn = identifier['identifier']
    return isbn


def search_from_daum_books(keyword):
    apikey = config['daum']['api_key']
    params = {
        'apikey': apikey,
        'output': 'json',
        'q': keyword,
        'searchType': 'isbn',
        'result': 1,
    }
    r = requests.get('https://apis.daum.net/search/book', params=params)
    result_dict = r.json()
    items = result_dict['channel']['item']
    item = items[0]
    return item


def search(request):
    books = []
    context = {
        'books': books
    }
    keyword = request.POST.get('keyword', '').strip()
    if keyword != '':
        google_result_dic = search_from_google_books(keyword)
        google_items = google_result_dic['items']

        for item in google_items:
            google_id = item['id']
            title = item['volumeInfo']['title']

            try:
                authors = item['volumeInfo']['authors'][0]
            except:
                authors = ''

            try:
                cover_thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
            except:
                try:
                    isbn = get_isbn_from_google_book(google_id)
                    daum_item = search_from_daum_books(isbn)
                    print(isbn)
                    cover_thumbnail = daum_item['cover_l_url']
                except:
                    cover_thumbnail = ''

            try:
                publisher = item['volumeInfo']['publisher']
            except:
                try:
                    isbn = get_isbn_from_google_book(google_id)
                    daum_item = search_from_daum_books(isbn)
                    print(isbn)
                    publisher = daum_item['pub_nm']
                except:
                    publisher = ''

            try:
                description = item['volumeInfo']['description']
            except:
                try:
                    isbn = get_isbn_from_google_book(google_id)
                    daum_item = search_from_daum_books(isbn)
                    print(isbn)
                    description = daum_item['description']
                except:
                    description = ''

            defaults = {
                'google_id': google_id,
                'title': title,
                'author': authors,
                'cover_thumbnail': cover_thumbnail,
                'publisher': publisher,
            }
            obj, created = Book.objects.get_or_create(
                description=description,
                defaults=defaults
            )
            print(obj)
            print(created)
            item_dict = {
                'title': title,
                'author': authors,
                'cover_thumbnail': cover_thumbnail,
                'publisher': publisher,
                'description': description,
                'google_id': google_id
            }
            books.append(item_dict)

    return render(request, 'book/index.html', context)
