import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.test import APITestCase, APILiveServerTestCase

User = get_user_model()


class TestUser(APITestCase, APILiveServerTestCase):
    def test_create_user(self):
        url = reverse('api:signup')
        data = {
            'username': 'test@test.com',
            'nickname': 'testnick',
            'password': 'testpassword'
        }
        hash_password = PBKDF2PasswordHasher()
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        self.assertEqual(User.objects.get().username, 'test@test.com')
        self.assertEqual(User.objects.get().nickname, 'testnick')
        # self.assertEqual(User.objects.get().password, hash_password)

    def test_login(self):
        url = reverse('api:signup')
        data = {
            'username': 'test@teat.com',
            'nickname': 'testnick',
            'password': 'testpassword',
        }
        response_sign = self.client.post(url, data, format='json')
        self.assertEqual(response_sign.status_code, status.HTTP_201_CREATED)

        url = reverse('api:login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        url = reverse('api:signup')
        data = {
            'username': 'test@teat.com',
            'nickname': 'testnick',
            'password': 'testpassword',
        }
        response_signup = self.client.post(url, data, format='json')
        self.assertEqual(response_signup.status_code, status.HTTP_201_CREATED)

        data = {
            'username': 'test@teat.com',
            'password': 'testpassword',
        }
        url = reverse('api:login')
        response_login = self.client.post(url, data)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)

        response_login_json = json.dumps(response_login.data)
        response_login_dict = json.loads(response_login_json)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + response_login_dict["key"])

        url = reverse('api:logout')
        response_login = client.post(url)
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
