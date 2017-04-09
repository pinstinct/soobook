from collections import OrderedDict

from rest_framework import pagination
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BookPagination(PageNumberPagination):
    page_size = 10


class MyBookPagination(PageNumberPagination):
    page_size = 9
    # ordering = '-update_date'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('userid', self.request.GET['userid']),
            ('results', data),
        ]))
