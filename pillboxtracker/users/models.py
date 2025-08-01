from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.constants import UsersConstants as uc


class CustomUser(AbstractUser):

    username = models.CharField(
        'Никнейм',
        max_length=uc.MAX_LENGTH.NAME,
        unique=True,
        help_text=uc.HELP_TEXT.NAME,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Никнейм не должен содержать данные символы - [w.@+-]+$'
        )]
    )
    email = models.EmailField(
        'email',
        max_length=uc.MAX_LENGTH.EMAIL,
        unique=True,
        help_text=uc.HELP_TEXT.EMAIL,
    )
    first_name = models.CharField(
        'Имя',
        max_length=uc.MAX_LENGTH.NAME,
        help_text=uc.HELP_TEXT.NAME,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=uc.MAX_LENGTH.NAME,
        help_text=uc.HELP_TEXT.NAME,
    )
    avatar = models.ImageField(
        'Аватар пользователя',
        upload_to='images_avatar/',
        blank=True,
        null=True,
    )
    gender = models.CharField(
        'Пол', max_length=uc.MAX_LENGTH.GENDER, blank=True
    )
    bio = models.TextField(
        'О себе:', max_length=uc.MAX_LENGTH.BIO,
        blank=True, help_text=uc.HELP_TEXT.BIO
    )
    birthday = models.DateField(
        'Дата рождения', blank=True, null=True,
        help_text=uc.HELP_TEXT.BIRTHDAY
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
    ]

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def get_age(self):
        today = date.today()
        birth_year = self.birthday.year
        age = today.year - birth_year
        if (today.month, today.day) < (self.birthday.month, self.birthday.day):
            age -= 1
        return age

    def __str__(self):
        return self.username
