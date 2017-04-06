from django.contrib.auth import get_user_model
from django.urls import NoReverseMatch
from django.urls import resolve
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIClient

from utils.auth_test import APIAuthMixin

User = get_user_model()


class MyBookAPITestCase(APILiveServerTestCase, APIAuthMixin):
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

    def test_book_add(self):
        client = APIClient()
        token = self.get_token(self.client)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        mybook_add_url = reverse('api:mybook')
        data = {
            'book_id': 'book_id'
        }
        response = client.post(mybook_add_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_book_delete(self):
        client = APIClient()
        token = self.get_token(self.client)
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        mybook_add_url = reverse('api:mybook')
        data = {
            'book_id': 'book_id'
        }
        response = client.delete(mybook_add_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_book_list(self):
        mybook_add_url = reverse('api:mybook')
        data = {
            'user_id': 'user_id'
        }
        response = self.client.get(mybook_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
