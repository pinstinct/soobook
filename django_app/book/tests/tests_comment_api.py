from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, APIClient

from book.models import MyBook
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

        # api : add
        data = {
            'mybook_id': dummy_mybook.pk,
            'content': '',
        }
        response = self.login_client.post(self.book_add_comment_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response['content'], data['content'])
