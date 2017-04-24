from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIClient

from book.models import MyBook, BookComment
from utils.auth_test import APIAuthMixin
from utils.book_test import APIBookMixin

User = get_user_model()


class MyBookCommentTestCase(APILiveServerTestCase, APIAuthMixin, APIBookMixin):
    def setUp(self):
        self.token = self.get_token(self.client)
        self.login_client = APIClient()
        self.login_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.book_add_comment_url = reverse('api:comment')

    @classmethod
    def create_dummy_mybook(cls, user, book):
        data = {
            'user': user,
            'book': book,
        }
        dummy_mybook = MyBook(**data)
        dummy_mybook.save()
        return dummy_mybook

    def test_comment_add(self):
        dummy_user = User.objects.get()
        dummy_book = self.create_dummy_book()
        dummy_mybook = self.create_dummy_mybook(dummy_user, dummy_book)

        data = {
            'mybook_id': dummy_mybook.pk,
            'content': '테스트코드테스트코드테스트코드',
        }
        response = self.login_client.post(self.book_add_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_detete(self):
        dummy_user = User.objects.get()
        dummy_book = self.create_dummy_book()
        dummy_mybook = self.create_dummy_mybook(dummy_user, dummy_book)

        data = {
            'mybook_id': dummy_mybook.pk,
            'content': '테스트코드테스트코드테스트코드',
        }
        response = self.login_client.post(self.book_add_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = {
            'comment_id': BookComment.objects.get(mybook_id=dummy_mybook.pk).pk,
        }
        response = self.login_client.delete(self.book_add_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
