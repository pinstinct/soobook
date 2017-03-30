from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^signup/$', apis.SignUpView.as_view()),
]
