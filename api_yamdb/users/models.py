from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'
ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class CustomUser(AbstractUser):
    """Кастомная модель юзера."""
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True,
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.CharField(
        verbose_name='Биография',
        blank=True, max_length=250,
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLES,
        max_length=10,
        default=USER,
        error_messages={'role': 'Неверная роль'}
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=100,
        null=True
    )

    @property
    def is_user(self):
        """Проверка. Пользователь 'user'?"""
        return self.role == USER

    @property
    def is_moderator(self):
        """Проверка. Пользователь 'moderator'?"""
        return self.role == MODERATOR

    @property
    def is_admin(self):
        """Проверка. Пользователь 'admin'?"""
        return self.role == ADMIN or self.is_superuser or self.is_staff

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}, {self.email}'
