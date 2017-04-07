from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class ModelAuthMixin(object):
    USERNAME = 'test@username.com'
    PASSWORD = '7890uiop'
    NICKNAME = 'dev'

    def create_user(self):
        user = User.objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD,
            nickname=self.NICKNAME,
        )
        return user


class APIAuthMixin(object):
    def get_token(self, client):
        signup_url = reverse('api:signup')
        data = {
            'username': 'test@username.com',
            'password': '7890uiop',
            'nickname': 'dev',
        }
        self.client.post(signup_url, data, format='json')

        login_url = reverse('api:login')
        data = {
            'username': 'test@username.com',
            'password': '7890uiop'
        }
        response = self.client.post(login_url, data, format='json')
        token = response.data.get('key')

        return token
