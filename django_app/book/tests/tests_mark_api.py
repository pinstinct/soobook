from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIClient

from book.models import MyBook, BookMark
from utils.auth_test import APIAuthMixin
from utils.book_test import APIBookMixin

User = get_user_model()


class MyBookMarkTestCase(APILiveServerTestCase, APIAuthMixin, APIBookMixin):
    def setUp(self):
        self.token = self.get_token(self.client)
        self.login_client = APIClient()
        self.login_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.book_mark_url = reverse('api:mark')

    @classmethod
    def create_dummy_mark(cls, user, book):
        data = {
            'user': user,
            'book': book,
        }
        dummy_mybook = MyBook(**data)
        dummy_mybook.save()
        return dummy_mybook

    def test_mark_add(self):
        dummy_user = User.objects.get()
        dummy_book = self.create_dummy_book()
        dummy_mybook = self.create_dummy_mark(dummy_user, dummy_book)

        data = {
            'mybook_id': dummy_mybook.pk,
            'content': '테스트코드테스트코드테스트코드',
        }
        response = self.login_client.post(self.book_mark_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_mark_update(self):
    #     dummy_user = User.objects.get()
    #     dummy_book = self.create_dummy_book()
    #     dummy_mybook = self.create_dummy_mark(dummy_user, dummy_book)
    #
    #     data = {
    #         'mark_id': get(mybook_id=dummy_mybook.id).id,
    #         'content': '책속 글귀 페이지 어쩌구 저쩌구',
    #     }
    #     response = self.login_client.put(self.book_mark_url, data)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_detete(self):
        dummy_user = User.objects.get()
        dummy_book = self.create_dummy_book()
        dummy_mybook = self.create_dummy_mark(dummy_user, dummy_book)

        data = {
            'mybook_id': dummy_mybook.pk,
            'content': '테스트코드테스트코드테스트코드',
        }
        response = self.login_client.post(self.book_mark_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'mark_id': BookMark.objects.get(mybook_id=dummy_mybook.pk).pk,
        }
        response = self.login_client.delete(self.book_mark_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
