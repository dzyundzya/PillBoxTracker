from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

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
        'Дата и время публикации', help_text=const.HELP_TEXT.PUB_DATE,
        default=timezone.now,
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

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'препарат'
        verbose_name_plural = 'Препараты'

    def __str__(self):
        return self.name

    def display_active_substance(self):
        return ', '.join(sorted([
            as_.name for as_ in self.active_substance.all()
        ]))

    def get_absolute_url(self):
        return reverse('pillbox:pill_detail', kwargs={'pill_id': self.pk})


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
        verbose_name = 'форма выпуска'
        verbose_name_plural = 'Формы выпуска'
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


class Like(GeneralModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Пользователь'
    )
    pill = models.ForeignKey(
        Pill,
        on_delete=models.CASCADE,
        related_name='likes',
        verbose_name='Препарат'
    )

    class Meta:
        unique_together = ('user', 'pill')
        verbose_name = 'лайк'
        verbose_name_plural = 'Лайки'


class Pillbox(models.Model):
    pill = models.ForeignKey(
        Pill, on_delete=models.SET_NULL, null=True,
        verbose_name='Препарат', related_name='pillboxes'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='pillboxes'
    )
    amount = models.PositiveSmallIntegerField(
        'Общее клоличество',
        validators=[
            MinValueValidator(const.MinValue.AMOUNT, message='Минимум одна'),
            MaxValueValidator(const.MaxValue.AMOUNT, message='Максимум двести')
        ],
        help_text=const.HELP_TEXT.AMOUNT,
    )
    daily_count = models.PositiveSmallIntegerField(
        'Количество в день',
        validators=[
            MinValueValidator(
                const.MinValue.DAILY_COUNT, message='Минимум одна'
            ),
            MaxValueValidator(
                const.MaxValue.DAILY_COUNT, message='Максимум тридцать'
            )
        ],
        help_text=const.HELP_TEXT.DAILY_COUNT,
    )
    start_date = models.DateField(
        'Дата начала приема',
        default=timezone.now,
        help_text=const.HELP_TEXT.START_DATE,
    )
    is_active = models.BooleanField(
        'Активен',
        default=True,
        help_text=const.HELP_TEXT.IS_ACTIVE,
    )
    reminder_time = models.ManyToManyField(
        'ReminderTime',
        verbose_name='Время напоминания',
        help_text=const.HELP_TEXT.REMINDER_TIME,
    )

    class Meta:
        verbose_name = 'Таблетница'
        verbose_name_plural = 'Таблетницы'
        ordering = ('-start_date',)

    def __str__(self):
        return f"{self.pill.name} - {self.user.username}"

    def remaining_days(self):
        """Расчет оставшихся дней приема."""
        if self.amount and self.daily_count:
            days = self.amount // self.daily_count
            if self.amount % self.daily_count != 0:
                return days + 1
            return days
        return 0

    def display_reminder_time(self):
        return ', '.join(sorted([
            str(rt_.time)[:5] for rt_ in self.reminder_time.all()
        ]))

    def get_absolute_url(self):
        return reverse(
            'pillbox:profile', kwargs={'username': self.user.username}
        )

    display_reminder_time.short_description = 'Время напоминания'


class ReminderTime(models.Model):
    time = models.TimeField(
        'Время'
    )

    class Meta:
        verbose_name = 'время напоминания'
        verbose_name_plural = 'Время напоминания'
        ordering = ('-time',)

    def __str__(self):
        return f'{self.time}'
    
