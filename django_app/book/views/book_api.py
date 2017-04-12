import requests

from book.models import Book
from config.settings import config

__all__ = (
    # 'search_from_google_books',
    'search',
)


def search_from_google_books(keyword, index=None):
    if index:
        index = index * 10
    else:
        index = 0
    key = config['google']['key']
    params = {
        'q': keyword,
        'langRestrict': 'ko',
        'maxResults': 10,
        'startIndex': index,
        'orderBy': 'relevance',
        'source': keyword,
        'key': key,
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


def get_description_from_google_book(google_id):
    params = {
        'volumeId': google_id
    }
    r = requests.get('https://www.googleapis.com/books/v1/volumes/volumeId', params=params)
    result_dict = r.json()
    google_description = result_dict['volumeInfo']['description']
    if google_description:
        description = google_description
    return description


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


def search(keyword, num):
    if keyword != '':
        for i in range(num):
            google_result_dic = search_from_google_books(keyword, i)
            google_items = google_result_dic['items']

            for item in google_items:
                google_id = item['id']
                title = item['volumeInfo']['title']

                # authors
                try:
                    authors = item['volumeInfo']['authors'][0]
                except:
                    authors = ''

                # cover_thumbnail
                try:
                    cover_thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
                except:
                    try:
                        isbn = get_isbn_from_google_book(google_id)
                        daum_item = search_from_daum_books(isbn)
                        # print(isbn)
                        cover_thumbnail = daum_item['cover_l_url']
                    except:
                        cover_thumbnail = ''

                # publisher
                try:
                    publisher = item['volumeInfo']['publisher']
                except:
                    try:
                        isbn = get_isbn_from_google_book(google_id)
                        daum_item = search_from_daum_books(isbn)
                        # print(isbn)
                        publisher = daum_item['pub_nm']
                    except:
                        publisher = ''

                # description
                try:
                    description = item['volumeInfo']['description']
                except:
                    try:
                        google_description = get_description_from_google_book(google_id)
                        description = google_description
                    except:
                        try:
                            isbn = get_isbn_from_google_book(google_id)
                            daum_item = search_from_daum_books(isbn)
                            # print(isbn)
                            description = daum_item['description']
                        except:
                            description = ''

                # 데이터베이스에 저장
                defaults = {
                    # 'google_id': google_id,
                    'title': title,
                    'author': authors,
                    'cover_thumbnail': cover_thumbnail,
                    'publisher': publisher,
                    'description': description,
                    'keyword': keyword,
                }
                obj, updated = Book.objects.update_or_create(
                    google_id=google_id,
                    description='',
                    defaults=defaults
                )
