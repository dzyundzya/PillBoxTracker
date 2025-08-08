from django.db import models


class Accordion(models.Model):
    title = models.CharField(
        'Заголовок кнопки', blank=True, null=True, max_length=100,
    )
    strong_text = models.CharField(
        'Заголовок вкладки', blank=True, null=True, max_length=100,
    )
    text = models.TextField(
        'Содержание вкладки', blank=True, null=True,
    )
    group = models.CharField(
        'Группа аккордеона', blank=True, null=True, max_length=30,
    )

    class Meta:
        verbose_name = 'поле аккордеона'
        verbose_name_plural = 'Аккордеон'

    def __str__(self):
        return self.title
