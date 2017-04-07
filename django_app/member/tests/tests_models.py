from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase

User = get_user_model()


class MemberModelTestCase(LiveServerTestCase):
    USERNAME = 'test@username.com'
    PASSWORD = 'test_password'
    NICKNAME = 'dev'

    def test_create_user(self):
        now_count = User.objects.count()
        User.objects.create_user(
            username=self.USERNAME,
            password=self.PASSWORD,
            nickname=self.NICKNAME,
        )
        update_count = User.objects.count()
        self.assertNotEqual(now_count, update_count)
