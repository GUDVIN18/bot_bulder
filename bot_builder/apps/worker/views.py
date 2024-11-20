from django.shortcuts import render
from apps.worker.models import Events
from apps.bot.models import BotUser, Bot_Message
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


@csrf_exempt
def task_complete_alert(request):

        # Получаем данные из запроса
        data = json.loads(request.body)
        task_id = data.get('id')
        answer = data.get('text_llm_models')
        
        # Получаем оригинальное событие по task_id
        original_event = Events.objects.get(task_id=task_id)
        user = original_event.user

        Events.objects.create(
            status='ACCEPTED',
            update_data={
                "message": {
                    "from": {
                        "id": user.tg_id,  # ID пользователя в Telegram
                        "username": user.username,  # Username пользователя
                        "first_name": user.first_name,  # Имя пользователя
                        "language_code": "ru",  # Язык пользователя
                        "is_premium": False  # Премиум статус
                    },
                    "text": f"{answer}",  # Текст сообщения
                    "chat": {
                        "id": user.tg_id  # ID чата (обычно совпадает с ID пользователя в личных сообщениях)
                    }
                }
            }
        )

        return HttpResponse("Все ок")

