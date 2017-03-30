from django.conf.urls import url
from rest_framework.authtoken import views

from .. import apis

urlpatterns = [
    url(r'^signup/$', apis.SignUpView.as_view()),
    url(r'^profile/$', apis.ProfileView.as_view()),
    url(r'^token-auth/', views.obtain_auth_token),
]
