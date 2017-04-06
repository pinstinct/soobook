from django.test import LiveServerTestCase

from book.models import Book


class BookModelTestCase(LiveServerTestCase):
    def test_create_book_with_POST_request(self):
        self.client.post(
            '/',
            data={'keyword': '파이썬'}
        )
        self.assertEqual(Book.objects.count(), 10)
