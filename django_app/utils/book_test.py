from book.models import Book


class APIBookMixin(object):
    @classmethod
    def create_dummy_book(cls, dummy_title=None):
        dummy_data = {
            'google_id': 'dummy_google_id',
            'title': dummy_title if dummy_title else 'dummy_title',
            'author': 'dummy_author',
            'cover_thumbnail': 'dummy_cover_thumbnail',
            'publisher': 'dummy_publisher',
            'description': 'dummy_description',
            'keyword': 'dummy_keyword',
        }
        dummy_book = Book(**dummy_data)
        dummy_book.save()
        return dummy_book

    @classmethod
    def create_dummy_book_list(cls, num_of_books):
        dummy_book_list = []
        for i in range(num_of_books):
            dummy_book = cls.create_dummy_book('dummy_title_{}'.format(i))
            dummy_book_list.append(dummy_book)
        return dummy_book_list
