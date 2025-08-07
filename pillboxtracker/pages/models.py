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
        'Группа аккардеона', blank=True, null=True, max_length=30,
    )

    def __str__(self):
        return self.title
