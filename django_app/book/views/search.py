import json

import requests
from dateutil.parser import parse
from django.shortcuts import render

from django_app.config.settings import config

google_api_key = config['google_book']['API_KEY']


def search_from_google(keyword):
    params = {
        'q': keyword,
        'key': google_api_key,
    }

    r = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
    result = r.text

    # 4. 해당 내용을 다시 json.loads()를 이용해 파이썬 객체로 변환
    result_dict = json.loads(result)
    return result_dict


def search(request):
    book = []
    context = {
        'book': book,
    }

    keyword = request.GET.get('keyword', '').strip()

    if keyword != '':
        # 검색 결과를 받아옴
        search_result = search_from_google(keyword)

        # 검색결과에서 이전/다음 토큰, 전체 결과 개수를 가져와
        # 템플릿에 전달할 context객체에 할당

        total_items = search_result.get('totalItems')

        context['totalItems'] = total_items
        context['keyword'] = keyword

        # 검색결과에서 'items'키를 갖는 list를 items변수에 할당 후 loop
        items = search_result['items']
        for item in items:
            published_date_str = item['volumeInfo']['publishedDate']

            # 실제로 사용할 데이터
            google_id = item['id']
            title = item['volumeInfo']['title']
            authors = item['volumInfo']['authors']
            description = item['volumeInfo']['description']
            publisher = item['voulumeInfo']['publisher']
            published_date = parse(published_date_str)
            cover_thumbnail = item['volumeInfo']['imageLinks']['thumbnail']
            # 이미 북마크에 추가된 영상인지 판단


            # 현재 item을 dict로 정리
            cur_item_dict = {
                'title': title,
                'description': description,
                'authors': authors,
                'published_date': published_date,
                'books_id': google_id,
                'url_thumbnail': cover_thumbnail,
                'publisher': publisher,
            }
            book.append(cur_item_dict)

    return render(request, 'video/search.html', context)