from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot.models import Bot_Message, Bot_Button, BotUser
from apps.worker.models import Events
import requests
from datetime import datetime
import pandas as pd
import time
from threading import Thread


class Bot_Handler():
    def __init__(self) -> None:
        self.val = {}  # Инициализируем словарь для хранения переменных


    def format_message_text(self, text):
        """Форматирует текст сообщения, подставляя значения из val"""
        try:
            # Проверяем, является ли text строкой
            if not isinstance(text, str):
                return str(text)
            return text.format(val=type('DynamicValue', (), self.val))
        except KeyError as e:
            print(f"Ошибка форматирования: переменная {e} не найдена")
            return text
        except Exception as e:
            print(f"Ошибка форматирования: {e}")
            return text




    def base(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)




    def start(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные
        print(f'''------------- START 
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем переменные для приветствия
        self.val['user_name'] = user.first_name if user.first_name is not None else user.username
        self.val['text'] = 'добро пожаловать'
        self.val['bot_name'] = 'Bot Builder'

        try:
            start_message = Bot_Message.objects.get(current_state='start')
            text = self.format_message_text(start_message.text)
        except Bot_Message.DoesNotExist:
            text = "Ошибка при получении состояния def start()"
            print(text)

        buttons = Bot_Button.objects.filter(message_trigger=start_message)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)


    def continue_message(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)




    def entering_preferences(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        
        message_text = message['text']

        user.state = state.current_state
        user.save()

        data = {
            'question': f"Пользователь {user.tg_id}: {message_text}",
            'task_end_handler': 'task_end_alert',
            # 'event_id': str(event.id)  # Добавляем ID события
        }

        response = requests.post('http://62.68.146.176:8092/create_task', data=data)

        bot.send_chat_action(chat_id=user.tg_id, action='typing', timeout=4)

        # Сохраняем task_id в событии
        event.task_id = response.json().get('task_id')  # Предполагая, что API возвращает task_id
        event.save()

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))
        

        bot.send_message(user.tg_id, text, reply_markup=keyboard)




    def success_LLM(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = message['text']

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)
    

