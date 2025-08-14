# [Создание платформера на Python, используя pygame](https://github.com/dzyundzya/platformer_pygame)

![Static Badge](https://img.shields.io/badge/author-Dzyundzya%20Alexandr-red
)
![Static Badge](https://img.shields.io/badge/celery-5.5.3-green
)
![Static Badge](https://img.shields.io/badge/python-3.9.13-blue
)
![Static Badge](https://img.shields.io/badge/django-3.2.16-black
)
![Static Badge](https://img.shields.io/badge/bootstrap-5-blue
)
![Static Badge](https://img.shields.io/badge/pytest-7.1.3-gray
)
![Static Badge](https://img.shields.io/badge/sqlite-orange
)


### Содержание:

1. [О проекте](#о-проекте)
2. [Интерфейс проекта](#интерфейс-проекта)
3. [Как запустить](#как-запустить)
4. [Проект сделал](#проект-сделал)
<br><hr>

## О проекте

Таблетница — это веб-приложение для эффективного управления лекарственными препаратами и их систематизации. Проект создан для помощи пользователям в организации и контроле приема медикаментов.

Проект «Таблетница» призван сделать процесс управления лекарствами более организованным и эффективным, помогая пользователям следить за своим здоровьем и своевременно принимать необходимые препараты.

* __Каталог препаратов:__ систематизированный список лекарств с подробными описаниями.<br>
* __Персональные списки:__ возможность создания индивидуальных таблеточниц.<br>
* __Система напоминаний:__ уведомления о необходимости приема препаратов с помощью Telegram-бота.<br>
* __Профили пользователей:__ личный кабинет с историей и настройками пользователя и администратора.<br>
* __Комментарии и отзывы:__ обмен опытом между пользователями.<br>

## Интерфейс проекта

<p float="left">
  <img src="README_images/login.png" width="33%" />
  <img src="README_images/about.png" width="25%" />
  <img src="README_images/rules.png" width="29%" />
</p>

## Как запустить
- $ pip install -r requirements.txt
- $ python manage.py migrate
- $ python manage.py createsuperuser
- $ python manage.py runserver
---
- $ celery -A pillboxtracker worker -l info --pool=threads --concurrency=4
- $ celery -A pillboxtracker beat -l info



## Проект сделал:
### [✍️ Dzyundzya Alexandr](https://github.com/dzyundzya)