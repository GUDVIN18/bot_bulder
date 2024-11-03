import requests
import time
from django.core.management.base import BaseCommand
from apps.bot.bot_core import tg_bot as bot_token
from apps.worker.models import Events
from apps.bot.models import BotUser, Bot_Commands, Bot_Message, Bot_Button
from telebot import TeleBot
from apps.worker.commands_handler import Bot_Handler
import importlib
from apps.worker.callback_handler import callback_handler



class Command(BaseCommand):
    def worker(bot):
        if Events.objects.filter(status='ACCEPTED').exists():
            states = Events.objects.filter(status='ACCEPTED')
            for state in states:
                update = state.update_data
                if 'message' in update:
                    message = update['message']
                    chat_id = message.get('from').get('id')
                    print(chat_id)
                    if 'text' in message:
                        if 'entities' in message:
                            for entity in message['entities']:
                                if entity['type'] == 'bot_command':
                                    # Получим тут список команд из модельки с командами
                                    commands = Bot_Commands.objects.all()
                                    
                                    print("Это команда:", message['text'])
                                    for command in commands:
                                        if command.text == message['text']:
                                            print('Команда найдена', command.trigger.text)

                                            bot_message = Bot_Message.objects.get(text=command.trigger.text)
                                            print(f'Привязанное сообщение к команде {bot_message.id} {bot_message.handler}')
                                            buttons = Bot_Button.objects.filter(message_trigger=bot_message)
                                            

                                            # Вытаскиваем название функции и вызывам ее 
                                            if bot_message.handler:
                                                try:
                                                    handler_function = getattr(Bot_Handler(), bot_message.handler)
                                                    handler_function(bot, chat_id, command.trigger.text, buttons)
                                                except Exception as e:
                                                    print('Ошибка', e)


                                        else:
                                            print('Команда не найдена')

                                    continue
                        else:        
                            print("Это текст:", message['text'])



                elif 'callback_query' in update:
                    callback_data = update['callback_query']['data']
                    user_id = update['callback_query']['from']['id']
                    print("\n\n ------ Это нажатие кнопки:", callback_data, user_id)
                    callback_handler(bot, callback_data, user_id)


                else:
                    print('Не обработанные данные')
                state.status = 'COMPLETED'
                state.save()




                




    while True:
        print('Запуск')
        worker(bot = TeleBot(bot_token))
        time.sleep(1)
        # time.sleep(0.1)




