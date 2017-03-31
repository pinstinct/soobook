from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^signup/$', apis.SignUp.as_view()),
    url(r'^login/$', apis.Login.as_view()),
    url(r'^logout/$', apis.Logout.as_view()),
]
