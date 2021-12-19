from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ Модель пользователя """
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Юзернэйм',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        max_length=150,
        unique=True,
        verbose_name='e-mail',
    )

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """ Модель для подписок на авторов """
    id = models.PositiveIntegerField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписки'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'following'],
            name='unique_following'
        )]
        verbose_name = 'Подписка'
