from django.conf.urls import url

from .. import apis

urlpatterns = [
    url(r'^signupios/$', apis.SignUpLogin.as_view(), name='signupios'),
    url(r'^signup/$', apis.SignUp.as_view(), name='signup'),
    url(r'^login/$', apis.Login.as_view(), name='login'),
    url(r'^logout/$', apis.Logout.as_view(), name='logout'),
]
