from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIClient

from book.models import MyBook
from utils.auth_test import APIAuthMixin
from utils.book_test import APIBookMixin

User = get_user_model()


class MyBookStarAPITestCase(APILiveServerTestCase, APIAuthMixin, APIBookMixin):
    def setUp(self):
        self.token = self.get_token(self.client)
        self.login_client = APIClient()
        self.login_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.mybook_add_url = reverse('api:mybook')
        self.book_star_add_url = reverse('api:star')
        self.book_star_list_url = reverse('api:star')

    def create_dummy_mybook(self, user, book):
        data = {
            'user': user,
            'book': book,
        }
        dummy_mybook = self.login_client.post(self.mybook_add_url, data)
        return dummy_mybook

    def test_star_add(self):
        dummy_book = self.create_dummy_book()
        # dummy_mybook = self.create_dummy_mybook(dummy_user, dummy_book)

        data = {
            'book_id': dummy_book.pk
        }
        dummy_mybook = self.login_client.post(self.mybook_add_url, data)
        self.assertEqual(dummy_mybook.status_code, status.HTTP_201_CREATED)

        # api : add
        data = {
            'mybook_id': MyBook.objects.get(book_id=dummy_book.id).id,
            'content': 1,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # api : update
        data = {
            'mybook_id': MyBook.objects.get(book_id=dummy_book.id).id,
            'content': 2.5,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # api : update
        data = {
            'mybook_id': MyBook.objects.get(book_id=dummy_book.id).id,
            'content': 5,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_star_add_validate_fail(self):
        dummy_book = self.create_dummy_book()
        data = {
            'book_id': dummy_book.pk
        }
        dummy_mybook = self.login_client.post(self.mybook_add_url, data)
        self.assertEqual(dummy_mybook.status_code, status.HTTP_201_CREATED)

        data = {
            'mybook_id': MyBook.objects.get(book_id=dummy_book.id).id,
            'content': -1,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['ios_error_code'], '4005')

        data = {
            'mybook_id': MyBook.objects.get(book_id=dummy_book.id).id,
            'content': 10,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['ios_error_code'], '4005')

    def test_star_add_field_requeired_fail(self):
        dummy_book = self.create_dummy_book()
        data = {
            'book_id': dummy_book.pk
        }
        dummy_mybook = self.login_client.post(self.mybook_add_url, data)
        self.assertEqual(dummy_mybook.status_code, status.HTTP_201_CREATED)

        data = {
            'mybook_id': None,
            'content': 5,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            'mybook_id': MyBook.objects.get(book_id=dummy_book.id).id,
            'content': None,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_star_add_field_invalid_mybook_fail(self):
        dummy_user = User.objects.get()
        dummy_book = self.create_dummy_book()
        dummy_mybook = self.create_dummy_mybook(dummy_user, dummy_book)

        data = {
            'mybook_id': 1000,
            'content': 5,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['ios_error_code'], '4004')

        data = {
            'mybook_id': -1,
            'content': 5,
        }
        response = self.login_client.post(self.book_star_add_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['ios_error_code'], '4004')
