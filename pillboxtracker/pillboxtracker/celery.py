import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pillboxtracker.settings')

app = Celery(
    'pillboxtracker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-pills-every-minute': {
        'task': 'pillbox.tasks.check_and_decrease_polls',
        'schedule': crontab(minute='*'),
    }
}

app.conf.update(
    CELERY_ENABLE_UTC=True,
    CELERY_TIMEZONE='Europe/Moscow'
)
