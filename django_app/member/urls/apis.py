from django.conf.urls import url

from .. import apis

urlpatterns = [
    # url(r'^signup/$', apis.SignUpView.as_view()),
    url(r'^signup/$', apis.SignUp.as_view()),
    url(r'^login/$', apis.Login.as_view()),
    # url(r'^profile/$', apis.ProfileView.as_view()),
    # url(r'^token-auth/', views.obtain_auth_token),
]
