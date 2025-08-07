import os
import requests
import logging

from dotenv import load_dotenv


load_dotenv()

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        if not self.token:
            raise ValueError("TELEGRAM_TOKEN не установлен в переменных окружения")
        self.base_url = f'https://api.telegram.org/bot{self.token}'

    def send_message(self, chat_id, text):
        try:
            params = {
                'chat_id': chat_id,
                'text': text
            }
            response = requests.post(f'{self.base_url}/sendMessage', params=params)
            result = response.json()
            if not result.get('ok'):
                logger.error(f"Ошибка Telegram API: {result.get('description')}")
                return False
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети при отправке сообщения: {str(e)}")
        except Exception as e:
            logger.error(f"Неизвестная ошибка при отправке сообщения: {str(e)}")

    def send_notification(self, user, message):
        try:
            if not user or not user.telegram_chat_id:
                logger.warning("Пользователь или chat_id не определены")
                return

            chat_id = user.telegram_chat_id
            logger.info(f"Отправка уведомления пользователю {chat_id}")

            result = self.send_message(chat_id, message)
            if result:
                logger.info("Сообщение успешно отправлено")
            else:
                logger.warning("Не удалось отправить сообщение")
        except Exception as e:
            logger.error(f"Критическая ошибка при отправке уведомления: {str(e)}")
            print(f'Ошибка отправки сообщения: {e}')
