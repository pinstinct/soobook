# import json
#
# import requests
# from dateutil.parser import parse
# from django.shortcuts import render
#
# from django_app.config.settings import config
#
# __all__ = (
#     'search_from_google',
#     'search'
# )
# google_api_key = config['google_book']['API_KEY']
#
#
# def search_from_google(keyword, ):
#     params = {
#         'q': keyword,
#         'key': google_api_key,
#     }
#
#     r = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
#     result = r.text
#
#     result_dict = json.loads(result)
#     return result_dict
#
#
# def search(request):
#     book = []
#     context = {
#         'book': book,
#     }
#
#     keyword = request.GET.get('keyword', '').strip()
#
#     if keyword != '':
#
#         search_result = search_from_google(keyword)
#
#         total_items = search_result.get('totalItems')
#
#         context['totalItems'] = total_items
#         context['keyword'] = keyword
#
#         items = search_result['items']
#         for item in items:
#             published_date_str = item['volumeInfo']['publishedDate']
#
#             google_id = item['id']
#             title = item['volumeInfo']['title']
#             authors = item['volumInfo']['authors']
#             description = item['volumeInfo']['description']
#             publisher = item['voulumeInfo']['publisher']
#             published_date = parse(published_date_str)
#             cover_thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
#
#             cur_item_dict = {
#                 'title': title,
#                 'description': description,
#                 'authors': authors,
#                 'published_date': published_date,
#                 'books_id': google_id,
#                 'url_thumbnail': cover_thumbnail,
#                 'publisher': publisher,
#             }
#             book.append(cur_item_dict)
#
#     return render(request, 'book/index.html', context)
