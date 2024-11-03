import requests
import time
from django.core.management.base import BaseCommand
from apps.bot.bot_core import tg_bot as bot
from apps.worker.models import Events
from apps.bot.models import BotUser


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
                        print(f'{update}\n\n')
                        # Обработка обновления
                        message = update.get("message", {})
                        chat_id = message.get("chat", {}).get("id")
                        text = message.get("text")
                        username = update.get('message', {}).get('from', {}).get('username')
                        first_name =  update.get('message', {}).get('from', {}).get('first_name')
                        language = update.get('message', {}).get('from', {}).get('language_code')
                        premium = update.get('message', {}).get('from', {}).get('premium')

                        Events.objects.create(
                            status='ACCEPTED',
                            update_data=update
                        )

                        # Обновление offset для получения следующего обновления
                        offset = update["update_id"] + 1

                else:
                    print("Ошибка при получении обновлений")
                time.sleep(0.05)  # Небольшая задержка между запросами

            except Exception as e:
                print(f"Произошла ошибка: {e}")
                time.sleep(1)  # Ожидание перед повторной попыткой в случае ошибки



    while True:
        long_polling(bot)