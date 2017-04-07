from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^search/$', apis.Search.as_view(), name='search'),
    url(r'^mybook/(?P<user_id>\d+)$', apis.MyBook.as_view(), name='mybook'),
    url(r'^mybook/$', apis.MyBook.as_view(), name='mybook'),
]