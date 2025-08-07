from datetime import timedelta
import logging

from celery import shared_task
from django.utils import timezone

from .models import Pillbox
from .telegram import TelegramBot


logging.basicConfig(
    level=logging.DEBUG,
    filename='tasks.log',
    filemode='w'
)

logger = logging.getLogger(__name__)


@shared_task(ignore_result=True, default_retry_delay=60, max_retries=3)
def check_and_decrease_polls():
    now_utc = timezone.now()
    now_local = now_utc.astimezone()
    bot = TelegramBot()

    try:
        active_pillboxes = Pillbox.objects.filter(is_active=True)
        logger.info(f'Найдено активных Pillbox: {active_pillboxes.count()}')

        for pillbox in active_pillboxes:
            logger.info(f'Обработка Pillbox ID:{pillbox.id}')
            reminder_times = pillbox.reminder_time.all()
            for reminder in reminder_times:
                check_time = now_local.replace(
                    hour=reminder.time.hour,
                    minute=reminder.time.minute,
                    second=0,
                    microsecond=0
                )
                logger.info(f"Текущее время: {now_local}, Время проверки: {check_time}")

                if now_local >= check_time and now_local < check_time + timedelta(minutes=1):
                    logger.info(f"Время приема наступило для Pillbox ID: {pillbox.id}")
                    pillbox.amount -= 1

                    if pillbox.amount == 0:
                        pillbox.is_active = False
                    pillbox.save()

                    message = (
                        f'⏰ Время приёма лекарства!\n'
                        f'Препарат: {pillbox.pill.name}\n'
                        f'Осталось таблеток: {pillbox.amount}\n'
                        f'Время приёма: {reminder.time}'
                    )
                    try:
                        bot.send_notification(pillbox.user, message)
                        logging.info(f'Уведомление отправлено для Pillbox ID: {pillbox.id}')
                    except Exception as e:
                        logger.error(f"Ошибка при отправке уведомления: {str(e)}")
                    break
    except Exception as e:
        logger.critical(f"Критическая ошибка: {str(e)}")