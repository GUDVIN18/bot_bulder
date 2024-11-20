import requests
import time
from django.core.management.base import BaseCommand
from apps.bot.bot_core import tg_bot as bot
from apps.worker.models import Events
from apps.bot.models import BotUser


# class Command(BaseCommand):

#     def long_polling(token):
#         url = f"https://api.telegram.org/bot{token}/getUpdates"
#         offset = 0
#         timeout = 30

#         while True:
#             try:
#                 response = requests.get(f"{url}?offset={offset}&timeout={timeout}")
#                 result = response.json()

#                 if result["ok"]:
#                     for update in result["result"]:
#                         print(f'{update}\n\n')
#                         # Обработка обновления
#                         message = update.get("message", {})
#                         chat_id = message.get("chat", {}).get("id")
#                         text = message.get("text")
#                         username = update.get('message', {}).get('from', {}).get('username')
#                         first_name =  update.get('message', {}).get('from', {}).get('first_name')
#                         language = update.get('message', {}).get('from', {}).get('language_code')
#                         premium = update.get('message', {}).get('from', {}).get('premium')

#                         Events.objects.create(
#                             status='ACCEPTED',
#                             update_data=update
#                         )

#                         # Обновление offset для получения следующего обновления
#                         offset = update["update_id"] + 1

#                 else:
#                     print("Ошибка при получении обновлений")
#                 time.sleep(0.05)  # Небольшая задержка между запросами

#             except Exception as e:
#                 print(f"Произошла ошибка: {e}")
#                 time.sleep(1)  # Ожидание перед повторной попыткой в случае ошибки



#     while True:
#         long_polling(bot)










class Command(BaseCommand):

    def long_polling(token):
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        offset = 0
        timeout = 30

        while True:
            try:
                response = requests.get(f"{url}?offset={offset}&timeout={timeout}")
                result = response.json()

                if result["ok"]:
                    for update in result["result"]:
                        # Обработка обновления
                        message = update.get("message", {})
                        chat_id = message.get("chat", {}).get("id")
                        text = message.get("text")
                        user_info = message.get("from", {})
                        user_id = user_info.get("id")  # Получаем user_id
                        username = user_info.get("username")
                        first_name = user_info.get("first_name")
                        language = user_info.get("language_code")
                        premium = user_info.get("premium")

                        # Создаем событие с добавлением user_id
                        Events.objects.create(
                            status='ACCEPTED',
                            update_data=update,
                        )

                        print(f'Обновление от пользователя {user_id} (username: {username}): {text}\n')

                        # Обновляем offset для получения следующего обновления
                        offset = update["update_id"] + 1

                else:
                    print("Ошибка при получении обновлений")
                time.sleep(0.05)

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                time.sleep(1)

    while True:
        long_polling(bot)
