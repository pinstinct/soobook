from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^search/$', apis.Search.as_view(), name='search'),
    url(r'^mybook/$', apis.MyBook.as_view(), name='mybook'),
    url(r'^mybook/detail/$', apis.MyBookDetail.as_view(), name='mybook_detail'),
    url(r'^mybook/search/$', apis.MyBookSearch.as_view(), name='mybook_search'),
    url(r'^comment/$', apis.Comment.as_view(), name='comment'),
    url(r'^star/$', apis.Star.as_view(), name='star'),
]
