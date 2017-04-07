from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book
from book.serializers import SearchSerializer
from book.views import search_from_google_books
from book.views.book_api import get_isbn_from_google_book, search_from_daum_books, get_description_from_google_book

__all__ = (
    'Search',
    'MyBook',
)


# 주현님
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 1000


class Search(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Book.objects.all()
    serializer_class = SearchSerializer
    pagination_class = StandardResultsSetPagination

    # @csrf_exempt
    # def list(self, request):
    #     keyword = request.GET['keyword']
    #     books = self.queryset.filter(keyword=keyword)
    #     serializer = SearchSerializer(books, many=True)
    #     return Response(serializer.data)

    def list(self, request):
        books = []

        keyword = request.GET['keyword']
        if keyword != '':
            google_result_dic = search_from_google_books(keyword)
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
                            description = daum_item['description']
                        except:
                            description = ''

                # 데이터베이스에 저장
                defaults = {

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
                item_dict = {
                    'title': title,
                    'author': authors,
                    'cover_thumbnail': cover_thumbnail,
                    'publisher': publisher,
                    'description': description,
                    'google_id': google_id
                }
                books.append(item_dict)

            books = Book.objects.filter(keyword=keyword)
            serializer = SearchSerializer(books, many=True)
            return Response(serializer.data)


class MyBook(APIView):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass
