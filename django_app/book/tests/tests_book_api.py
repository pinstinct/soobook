from django.urls import NoReverseMatch
from django.urls import resolve
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIClient

from book.models import MyBook
from utils.auth_test import APIAuthMixin
from utils.book_test import APIBookMixin


class MyBookAPITestCase(APILiveServerTestCase, APIAuthMixin, APIBookMixin):
    def setUp(self):
        self.token = self.get_token(self.client)
        self.login_client = APIClient()
        self.login_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.mybook_add_url = reverse('api:mybook')
        self.mybook_list_url = reverse('api:mybook')
        self.mybook_delete_url = reverse('api:mybook')
        self.mybook_detail_url = reverse('api:mybook_detail')

    def test_mybook_list_one_data(self):
        dummy_book = self.create_dummy_book()

        # api : post
        data = {
            'book_id': dummy_book.pk
        }
        response = self.login_client.post(self.mybook_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(MyBook.objects.all()), 1)

        # api : get
        response = self.login_client.get(self.mybook_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Todo : 반환 데이터 검증 방법 찾기
        self.assertEqual(response.data['count'], 1)
        # self.assertEqual(response.data['results']['mybook_id'], 1)
        # self.assertEqual(response.data['results']['mybook_id']['book']['id'], dummy_book.pk)
        # self.assertEqual(response.data['results']['mybook_id']['book']['title'], dummy_book.title)
        # self.assertEqual(response.data['results']['mybook_id']['book']['author'], dummy_book.author)
        # self.assertEqual(response.data['results']['mybook_id']['book']['cover_thumbnail'], dummy_book.cover_thumbnail)
        # self.assertEqual(response.data['results']['mybook_id']['book']['publisher'], dummy_book.publisher)
        # self.assertEqual(response.data['results']['mybook_id']['book']['description'], dummy_book.description)
        # self.assertEqual(response.data['results']['mybook_id']['book']['keyword'], dummy_book.keyword)

        # api : delete
        data = {
            'book_id': dummy_book.pk
        }
        response = self.login_client.delete(self.mybook_delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(MyBook.objects.all()), 0)

    def test_mybook_list_many_data(self):
        num_of_dummy_books = 10
        dummy_book_list = self.create_dummy_book_list(num_of_dummy_books)

        # api : post
        for i, dummy_book in enumerate(dummy_book_list, 1):
            data = {
                'book_id': dummy_book.pk
            }
            response = self.login_client.post(self.mybook_add_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(len(MyBook.objects.all()), i)

        # api : get
        response = self.login_client.get(self.mybook_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], num_of_dummy_books)

        # api : delete
        for i, dummy_book in enumerate(dummy_book_list, 1):
            data = {
                'book_id': dummy_book.pk
            }
            response = self.login_client.delete(self.mybook_delete_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(MyBook.objects.all()), num_of_dummy_books - i)

        self.assertEqual(len(MyBook.objects.all()), 0)

    def test_mybook_detail(self):
        dummy_book = self.create_dummy_book()

        # api : post
        data = {
            'book_id': dummy_book.pk
        }
        response = self.login_client.post(self.mybook_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # api : get : datail
        data = {
            'bookid': dummy_book.pk
        }
        response = self.login_client.get(self.mybook_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Todo : 반환 데이터 검증 방법 찾기
        # self.assertEqual(dummy_book.pk, response.data[0])
        # print(response.data)


class MyBookSearchAPITestCase(APILiveServerTestCase, APIAuthMixin):
    def test_apis_url_exists(self):
        try:
            resolve('/api/book/search/')
            resolve('/api/book/mybook/')
        except NoReverseMatch as e:
            self.fail(e)

    def test_book_search(self):
        keyword = 'python'
        book_search_url = reverse('api:search')
        url = '{}?keyword={}'.format(
            book_search_url,
            keyword
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
