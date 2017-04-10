from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from book.models import Book


class MyUserManager(BaseUserManager):
    def create_user(self, username, nickname, password=None):
        user = self.model(
            username=username,
            nickname=nickname,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, nickname, password):
        user = self.model(
            username=username,
            nickname=nickname,
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(unique=True, max_length=256)
    nickname = models.CharField(max_length=256)
    is_staff = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    # mybook = models.ManyToManyField(
    #     Book
    # )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'nickname',
    ]

    objects = MyUserManager()

    def __str__(self):
        return '{},{}'.format(
            self.username,
            self.nickname,
        )

    def get_full_name(self):
        return '{},{}'.format(
            self.nickname,
            self.username
        )

    def get_short_name(self):
        return self.nickname
