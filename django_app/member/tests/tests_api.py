from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
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
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        self.assertEqual(User.objects.get().username, 'test@test.com')
        self.assertEqual(User.objects.get().nickname, 'testnick')
        self.assertEqual(User.objects.get().password, 'testpassword')
