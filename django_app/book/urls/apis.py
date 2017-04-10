from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^search/$', apis.Search.as_view(), name='search'),
    url(r'^mybook/$', apis.MyBook.as_view(), name='mybook'),
    url(r'^comment/$', apis.Comment.as_view(), name='comment'),
    url(r'^star/$', apis.Star.as_view(), name='star'),
]
