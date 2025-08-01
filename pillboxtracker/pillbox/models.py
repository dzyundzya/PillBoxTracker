from django.contrib.auth import get_user_model
from django.db import models

from .constants import PillboxConstants as const

User = get_user_model()


class GeneralModel(models.Model):
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Pill(GeneralModel):
    name = models.CharField(
        'Название препарата', max_length=const.MAX_LENGTH.NAME
    )
    description = models.TextField('Описание')
    pub_date = models.DateTimeField(
        'Дата и время публикации', help_text=const.HELP_TEXT.PUB_DATE
    )
    manufacturer = models.ForeignKey(
        'Manufacturer', on_delete=models.SET_NULL, null=True,
        verbose_name='Производитель', related_name='pills'
    )
    medicine_form = models.ForeignKey(
        'MedicineForm', on_delete=models.SET_NULL, null=True,
        verbose_name='Форма выпуска',
        related_name='pills'
    )
    active_substance = models.ManyToManyField(
        'ActiveSubstance',
        verbose_name='Действующее вещество',
        related_name='pills'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор публикации', related_name='pills'
    )
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True,
        related_name='pills', verbose_name='Категория'
    )
    image = models.ImageField(
        'Изображение препарата', upload_to='pill_image', blank=True
    )
    is_published = models.BooleanField(
        'Опубликовано', default=True,
        help_text=const.HELP_TEXT.IS_PUBLISHED
    )

    def __str__(self):
        return self.name


class ActiveSubstance(GeneralModel):
    name = models.CharField(
        'Действующее вещество', max_length=const.MAX_LENGTH.NAME
    )
    slug = models.SlugField(
        'Идентификатор действующего вещества', unique=True,
        help_text=const.HELP_TEXT.SLUG
    )

    class Meta:
        verbose_name = 'действующее вещество'
        verbose_name_plural = 'Действующее вещество'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='unique_active_substance'
            )
        ]

    def __str__(self):
        return self.name


class Manufacturer(GeneralModel):
    name = models.CharField('Название', max_length=const.MAX_LENGTH.NAME)
    country = models.CharField('Страна', max_length=const.MAX_LENGTH.COUNTRY)

    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return self.name


class MedicineForm(GeneralModel):
    name = models.CharField('Форма выпуска', max_length=const.MAX_LENGTH.NAME)
    slug = models.SlugField(
        'Идентификатор формы выпуска', unique=True,
        help_text=const.HELP_TEXT.SLUG
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'slug'],
                name='uniqueform'
            )
        ]

    def __str__(self):
        return self.name


class Category(GeneralModel):
    title = models.CharField(
        'Заголовок категории', max_length=const.MAX_LENGTH.NAME
    )
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор категории', unique=True,
        help_text=const.HELP_TEXT.SLUG
    )
    is_published = models.BooleanField(
        'Опубликовано', default=True,
        help_text=const.HELP_TEXT.IS_PUBLISHED
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'slug'],
                name='uniquecategory'
            )
        ]

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField('Текст комментария')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    pill = models.ForeignKey(
        Pill, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Комментируемый препарат'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Автор комментария'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)
