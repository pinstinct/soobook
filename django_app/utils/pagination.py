import collections
import re

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BookPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        p = '^http:'

        next_i = self.get_next_link()
        if next_i is None:
            next_url = None
        else:
            next_url = re.sub(p, 'https:', next_i)

        previous_i = self.get_previous_link()
        if previous_i is None:
            previous_url = None
        else:
            previous_url = re.sub(p, 'https:', previous_i)

        ret = collections.OrderedDict()
        ret["count"] = self.page.paginator.count
        ret["next"] = next_url
        ret["previous"] = previous_url
        ret["results"] = data
        return Response(ret)


class MyBookPagination(PageNumberPagination):
    page_size = 12

    def get_paginated_response(self, data):
        p = '^http:'

        next_i = self.get_next_link()
        if next_i is None:
            next_url = None
        else:
            next_url = re.sub(p, 'https:', next_i)

        previous_i = self.get_previous_link()
        if previous_i is None:
            previous_url = None
        else:
            previous_url = re.sub(p, 'https:', previous_i)

        ret = collections.OrderedDict()
        ret["count"] = self.page.paginator.count
        ret["next"] = next_url
        ret["previous"] = previous_url
        ret["results"] = data
        return Response(ret)
