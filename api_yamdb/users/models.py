from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class MyUser(AbstractUser):
    email = models.EmailField('email', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        'Роль', max_length=25, choices=Role.choices, default=Role.USER
    )
    confirmation_code = models.CharField(max_length=30, blank=True)

    @property
    def is_user(self):
        return self.role == Role.USER

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR
