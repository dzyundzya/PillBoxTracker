class PillboxConstants:
    class PAGINATION:
        PILL = 10
        PILLBOX = 3

    class MAX_LENGTH:
        NAME = 256
        COUNTRY = 100

    class HELP_TEXT:
        NAME = 'Обязательно для заполнения, не более 150 символов.'
        IS_PUBLISHED = 'Снимите галочку, чтобы скрыть публикацию.'
        PUB_DATE = 'Если установить дату и время в будущем — можно делать отложенные публикации.'
        SLUG = 'Идентификатор; разрешены символы латиницы, цифры, дефис и подчёркивание.'
        AMOUNT = 'Общее количество приема препарата в шт., от 1 до 200'
        DAILY_COUNT = 'Количесто приема препарата в день в шт., от 1 до 30'
        START_DATE = 'Дата, с которой начинается прием препарата'
        IS_ACTIVE = 'Статус активности схемы приема'
        REMINDER_TIME = 'Время, когда нужно принимать препарат'

    class MinValue:
        AMOUNT = 1
        DAILY_COUNT = 1

    class MaxValue:
        AMOUNT = 200
        DAILY_COUNT = 30
