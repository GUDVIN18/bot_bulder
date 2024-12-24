from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from apps.bot.models import Bot_Message, Bot_Button, BotUser
from apps.worker.models import Events
import requests
from datetime import datetime
import pandas as pd
import time
from threading import Thread
import os
import requests
from django.core.files import File




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

        bot.send_message(user.tg_id, text, reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True)
        


    
    def new_photo_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        if user.tg_id in [6424595615, 1066043357]:
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


        
    def new_photo_suc(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()

        # Получаем файл с максимальным разрешением
        file_id = message['photo'][-1]['file_id']   # Последний элемент - фото в лучшем качестве
        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'

        # Загружаем фото с сервера Telegram
        response = requests.get(file_url, stream=True)
        if response.status_code == 200:
            # Определяем имя файла
            file_name = f"user_photo_{user.id}.jpg"
            file_path = f'/root/project/bot_bulder/bot_builder/media/{file_name}'  # Каталог сохранения

            # Сохраняем файл локально
            with open(file_path, 'wb') as f:
                f.write(response.content)

            # Обновляем поле photo пользователя
            with open(file_path, 'rb') as f:
                user.photo.save(file_name, File(f))
                user.save()

            bot.send_message(user.tg_id, "Фото успешно сохранено.")
        else:
            bot.send_message(user.tg_id, "Не удалось загрузить фото.")

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



    def new_promt_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        if user.tg_id in [6424595615, 1066043357]:
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




    def new_promt_send(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        
        message_text = message['text']
        user.prompt = message_text

        user.state = state.current_state
        user.save()

       

        # Данные, которые отправляются в запросе
        data_horizontally = {
            'user_id': user.tg_id,
            'prompt': message_text,
            'format_photo': 'Горизонтальный',
            'task_end_handler': 'task_end_alert',
            'generation_or_face_to_face': 'True',
        }
        # Данные, которые отправляются в запросе
        data_vertically = {
            'user_id': user.tg_id,
            'prompt': message_text,
            'format_photo': 'Вертикальный',
            'task_end_handler': 'task_end_alert',
            'generation_or_face_to_face': 'True',
        }

        for _ in range(3):
            # Открываем файл заново на каждой итерации
            with open(user.photo.path, 'rb') as file:
                files = {'user_photo': file}

                # Отправляем запрос
                response = requests.post('http://91.218.245.239:8091/create_task', data=data_horizontally, files=files)
                time.sleep(0.2)

                # Проверяем ответ сервера
                if response.status_code == 200:
                    print("Задача успешно создана:", response.json())
                else:
                    print(f"Ошибка: {response.status_code}, {response.text}")

        
        for _ in range(3):
            # Открываем файл заново на каждой итерации
            with open(user.photo.path, 'rb') as file:
                files = {'user_photo': file}

                # Отправляем запрос
                response = requests.post('http://91.218.245.239:8091/create_task', data=data_vertically, files=files)
                time.sleep(0.2)

                # Проверяем ответ сервера
                if response.status_code == 200:
                    print("Задача успешно создана:", response.json())
                else:
                    print(f"Ошибка: {response.status_code}, {response.text}")


        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))
        
        # Отправляем сообщение
        bot.send_message(user.tg_id, text, reply_markup=keyboard)





    def send_10(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        if user.tg_id in [6424595615, 1066043357]:
            user.state = state.current_state
            user.save()

            # Данные, которые отправляются в запросе
            data = {
                'user_id': user.tg_id,
                'prompt': message['text'],
                'format_photo': user.format_photo,
                'task_end_handler': 'task_end_alert',
                'generation_or_face_to_face': 'True',
            }

            for _ in range(10):
                # Открываем файл заново на каждой итерации
                with open(user.photo.path, 'rb') as file:
                    files = {'user_photo': file}

                    # Отправляем запрос
                    response = requests.post('http://91.218.245.239:8091/create_task', data=data, files=files)
                    time.sleep(0.2)

                    # Проверяем ответ сервера
                    if response.status_code == 200:
                        print("Задача успешно создана:", response.json())
                    else:
                        print(f"Ошибка: {response.status_code}, {response.text}")

                # Форматируем текст с использованием переменных
                text = self.format_message_text(state.text)

                buttons = Bot_Button.objects.filter(message_trigger=state)
                keyboard = InlineKeyboardMarkup()
                for button in buttons:
                    keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))
                
                # Отправляем сообщение
                bot.send_message(user.tg_id, text, reply_markup=keyboard)













    # #Опрос start
    # def start_opros(self, bot, state, user, callback_data, callback_id, message, event):
    #     self.val = {}  # Очищаем переменные для каждого нового вызова
    #     print(f'''
    #         user - {user}
    #         call_data - {callback_data}
    #         call_id - {callback_id}
    #         message - {message}''')

    #     user.state = state.current_state
    #     user.save()

    #     # Добавляем базовые переменные
    #     self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
    #     self.val['user_id'] = user.tg_id
    #     self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

    #     # Форматируем текст с использованием переменных
    #     text = self.format_message_text(state.text)

    #     buttons = Bot_Button.objects.filter(message_trigger=state)
    #     keyboard = InlineKeyboardMarkup()
    #     for button in buttons:
    #         keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))


    #     sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

    #     # Сохраняем его ID в пользовательскую модель или в state
    #     user.last_message_id = sent_message.message_id
    #     user.save()


    #Выбор суммы
    def start_opros(self, bot, state, user, callback_data, callback_id, message, event):
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

        # buttons = Bot_Button.objects.filter(message_trigger=state)
        # keyboard = InlineKeyboardMarkup()
        # for button in buttons:
        #     keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))

        buttons = Bot_Button.objects.filter(message_trigger=state)
        top_row = buttons[:3]
        bottom_row = buttons[3:6]

        keyboard = InlineKeyboardMarkup()

        # Добавляем первые три кнопки в одну строку
        keyboard.row(*(InlineKeyboardButton(text=btn.text, callback_data=f'{btn.data} {btn.text}') for btn in top_row))

        # Добавляем следующие три кнопки во вторую строку
        keyboard.row(*(InlineKeyboardButton(text=btn.text, callback_data=f'{btn.data} {btn.text}') for btn in bottom_row))


        sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        # Сохраняем его ID в пользовательскую модель или в state
        user.last_message_id = sent_message.message_id
        user.save()





    # Выбранная сумма
    def summa_invest_user(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')


        user.summa = callback_data.split(' ')[1]

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)


        buttons = Bot_Button.objects.filter(message_trigger=state)
        top_row = buttons[:3]
        bottom_row = buttons[3:5]

        keyboard = InlineKeyboardMarkup()

        # Добавляем первые три кнопки в одну строку
        keyboard.row(*(InlineKeyboardButton(text=btn.text, callback_data=f'{btn.data} {btn.text}') for btn in top_row))

        # Добавляем следующие три кнопки во вторую строку
        keyboard.row(*(InlineKeyboardButton(text=btn.text, callback_data=f'{btn.data} {btn.text}') for btn in bottom_row))

        if user.last_message_id:
            # Убираем кнопки у предыдущего сообщения, установив reply_markup=None
            bot.edit_message_reply_markup(chat_id=user.tg_id, 
                                        message_id=user.last_message_id, 
                                        reply_markup=None)

        sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        # Сохраняем его ID в пользовательскую модель или в state
        user.last_message_id = sent_message.message_id
        user.save()




    # Выбранное время
    def time_invest_user(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')


        user.period = callback_data.split(' ')[1]

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        top_row = buttons[:2]
        bottom_row = buttons[2:4]
        center_row = buttons[4:6]

        keyboard = InlineKeyboardMarkup()

        # Добавляем первые три кнопки в одну строку
        keyboard.row(*(InlineKeyboardButton(text=btn.text, callback_data=f'{btn.data} {btn.text}') for btn in top_row))

        # Добавляем следующие три кнопки во вторую строку
        keyboard.row(*(InlineKeyboardButton(text=btn.text, callback_data=f'{btn.data} {btn.text}') for btn in bottom_row))

        keyboard.row(*(InlineKeyboardButton(text=btn.text, callback_data=f'{btn.data} {btn.text}') for btn in center_row))

        if user.last_message_id:
            # Убираем кнопки у предыдущего сообщения, установив reply_markup=None
            bot.edit_message_reply_markup(chat_id=user.tg_id, 
                                        message_id=user.last_message_id, 
                                        reply_markup=None)

        sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        # Сохраняем его ID в пользовательскую модель или в state
        user.last_message_id = sent_message.message_id
        user.save()




   # Выбранный интерес
    def interests_user(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')


        user.interes = callback_data.split(' ')[1]

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
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))

        if user.last_message_id:
            # Убираем кнопки у предыдущего сообщения, установив reply_markup=None
            bot.edit_message_reply_markup(chat_id=user.tg_id, 
                                        message_id=user.last_message_id, 
                                        reply_markup=None)

        sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        # Сохраняем его ID в пользовательскую модель или в state
        user.last_message_id = sent_message.message_id
        user.save()




   # Выбранный тип инвестора
    def type_investor(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')


        user.type_investor = callback_data.split(' ')[1]

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        top_row = buttons[:2]

        keyboard = InlineKeyboardMarkup()

        # Добавляем первые три кнопки в одну строку
        keyboard.row(*(InlineKeyboardButton(text=btn.text, callback_data=f'{btn.data} {btn.text}') for btn in top_row))

    
        if user.last_message_id:
            # Убираем кнопки у предыдущего сообщения, установив reply_markup=None
            bot.edit_message_reply_markup(chat_id=user.tg_id, 
                                        message_id=user.last_message_id, 
                                        reply_markup=None)

        sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        # Сохраняем его ID в пользовательскую модель или в state
        user.last_message_id = sent_message.message_id
        user.save()




   # Выбранный гендер
    def gender_user(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.gender = callback_data.split(' ')[1]
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
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))

        if user.last_message_id:
            # Убираем кнопки у предыдущего сообщения, установив reply_markup=None
            bot.edit_message_reply_markup(chat_id=user.tg_id, 
                                        message_id=user.last_message_id, 
                                        reply_markup=None)

        sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        # Сохраняем его ID в пользовательскую модель или в state
        user.last_message_id = sent_message.message_id
        user.save()







   # Выбранная ориентация
    def text_in_front_photo(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.format_photo = callback_data.split(' ')[1]
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
        keyboard.add(InlineKeyboardButton(text='Загрузить фото', web_app=WebAppInfo(url=f'https://bcs-invest-balanser.site/user_photo_upload?tg_id={user.tg_id}')))
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))

        if user.last_message_id:
            # Убираем кнопки у предыдущего сообщения, установив reply_markup=None
            bot.edit_message_reply_markup(chat_id=user.tg_id, 
                                        message_id=user.last_message_id, 
                                        reply_markup=None)

        sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        # sent_message = bot.send_photo(
        #     chat_id=user.tg_id, 
        #     photo=open('/root/project/bot_bulder/bot_builder/media/primer.jpg', 'rb'), 
        #     caption=text,
        #     parse_mode='HTML',
        #     reply_markup=keyboard
        # )


        # Сохраняем его ID в пользовательскую модель или в state
        user.last_message_id = sent_message.message_id
        user.save()






    # Успешное фото
    def opros_photo_user(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        # user.count_generation += 1
        # user.save()

        # if user.summa_first == None or user.summa_first == '':
        #     user.summa_first = user.summa
        #     user.period_first = user.period
        #     user.interes_first = user.interes
        #     user.type_investor_first = user.type_investor
        #     user.gender_first = user.gender
        #     user.save()
        


        # try:

            # # Получаем файл с максимальным разрешением
            # file_id = message['photo'][-1]['file_id']   # Последний элемент - фото в лучшем качестве
            # file_info = bot.get_file(file_id)
            # file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'

            # # Загружаем фото с сервера Telegram
            # response = requests.get(file_url, stream=True)
            # if response.status_code == 200:
            #     # Определяем имя файла
            #     file_name = f"user_photo_{user.id}.jpg"
            #     file_path = f'/root/project/bot_bulder/bot_builder/media/{file_name}'  # Каталог сохранения

            #     # Сохраняем файл локально
            #     with open(file_path, 'wb') as f:
            #         f.write(response.content)

            #     # Обновляем поле photo пользователя
            #     with open(file_path, 'rb') as f:
            #         user.photo.save(file_name, File(f))
            #         user.save()



                # with open(user.photo.path, 'rb') as file:
                #     files = {'user_photo': file}

                #     data = {
                #         'user_id': user.tg_id,
                #         'prompt': f'promt_user {user.summa}_{user.period}_{user.interes}_{user.type_investor}_{user.gender}_{user.format_photo}',
                #         'format_photo': user.format_photo,
                #         'task_end_handler': 'task_end_alert',
                #         'generation_or_face_to_face': 'False',
                #     }
                #     response = requests.post('http://91.218.245.239:8091/create_task', data=data, files=files)

                #     if response.status_code == 200:
                #         print("Задача успешно создана:", response.json())
                #     else:
                #         print(f"Ошибка: {response.status_code}, {response.text}")

                    
            # else:
            #     bot.send_message(user.tg_id, "Не удалось загрузить фото.")



           
        # except Exception as e:
        #     bot.send_message(user.tg_id, f"Ошибка! Отправьте фото - {e}")

        #     return

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data}'))


        sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        # Сохраняем его ID в пользовательскую модель или в state
        user.last_message_id = sent_message.message_id
        user.save()





    def log_discharge(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.state = state.current_state
        user.save()


        response = requests.post('http://91.218.245.239:8091/get_logs')
        if response.status_code != 200:
            print(f"Ошибка получения файла: {response.status_code}")
            bot.send_message(user.tg_id, "Ошибка при получении файла")
            return
        file_path = "/root/project/bot_bulder/xlsx/log.xlsx"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # строка 729

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



        with open(file_path, 'wb') as file:
            file.write(response.content)

        if os.path.getsize(file_path) > 0:  # Проверяем, что файл не пустой
            with open(file_path, 'rb') as file:
                bot.send_document(chat_id=user.tg_id, document=file)
        else:
            bot.send_message(user.tg_id, "Файл пустой")



   # ошибка
    def after_error_send_photo(self, bot, state, user, callback_data, callback_id, message, event):
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
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))


        bot.send_photo(
            chat_id=user.tg_id, 
            photo=open('/root/project/bot_bulder/bot_builder/media/primer.jpg', 'rb'), 
            caption=text,
            parse_mode='HTML',
            reply_markup=keyboard
        )






   # поделиться ботом
    def invite_bot(self, bot, state, user, callback_data, callback_id, message, event):
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

        # Кнопка для шеринга с предустановленным текстом
        share_url = f"https://t.me/share/url?url=&text=Привет!%20👋"
        share_button = InlineKeyboardButton(
            text="Поделиться 📤", 
            url=share_url # URL для открытия окна шеринга с текстом
        )
        keyboard.add(share_button)

        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))


        bot.send_message(user.tg_id, text, reply_markup=keyboard)





    def start_generator(self, bot, state, user, callback_data, callback_id, message, event):
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
        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)






    def generator_leo_input_negative(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')


        user.prompt_leonardo = message['text']
        user.state = state.current_state
        user.save()


        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)




    def format_photo_leonardo(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        

        user.negative_prompt = message['text']
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
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)




   # Выбранная ориентация
    def format_photo_leonardo_btn(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')

        user.format_photo = callback_data.split(' ')[1]
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
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))


        # sent_message = bot.send_message(user.tg_id, text, reply_markup=keyboard)

        bot.send_photo(
            chat_id=user.tg_id, 
            photo=open('/root/project/bot_bulder/bot_builder/media/primer.jpg', 'rb'), 
            caption=text,
            parse_mode='HTML',
            reply_markup=keyboard
        )


    def send_leonardo_photo(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        if user.tg_id in [6424595615, 1066043357]:
            user.state = state.current_state
            user.save()
            try:
                # Получаем файл с максимальным разрешением
                file_id = message['photo'][-1]['file_id']   # Последний элемент - фото в лучшем качестве
                file_info = bot.get_file(file_id)
                file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'


                # Загружаем фото с сервера Telegram
                response = requests.get(file_url, stream=True)
                if response.status_code == 200:
                    # Определяем имя файла
                    file_name = f"user_photo_leonardo_{user.id}.jpg"
                    file_path = f'/root/project/bot_bulder/bot_builder/media/{file_name}'  # Каталог сохранения

                    # Сохраняем файл локально
                    with open(file_path, 'wb') as f:
                        f.write(response.content)

                    # Обновляем поле photo пользователя
                    with open(file_path, 'rb') as f:
                        user.photo.save(file_name, File(f))
                        user.save()



                    with open(user.photo.path, 'rb') as file:
                        files = {'user_photo': file}

                        data = {
                            'user_id': user.tg_id,
                            'prompt': user.prompt_leonardo,
                            'negative_prompt': user.negative_prompt,
                            'format_photo': user.format_photo,

                        }
                        response = requests.post('http://91.218.245.239:8091/start_leonardo_generations', data=data, files=files)

                        if response.status_code == 200:
                            print("Задача успешно создана: ", response.json())
                            bot.send_message(user.tg_id, "Ожидайте")

                        
                else:
                    bot.send_message(user.tg_id, "Не удалось загрузить фото.")



            
            except Exception as e:
                bot.send_message(user.tg_id, f"Ошибка! Отправьте фото - {e}")

                return




            # Добавляем базовые переменные
            self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
            self.val['user_id'] = user.tg_id
            self.val['text'] = 'Базовое сообщение'  # Значение по умолчанию

            # Форматируем текст с использованием переменных
            text = self.format_message_text(state.text)

            buttons = Bot_Button.objects.filter(message_trigger=state)
            keyboard = InlineKeyboardMarkup()
            for button in buttons:
                keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))

            bot.send_message(user.tg_id, text, reply_markup=keyboard)









    #Замена лиц 10 фоток 
    def face_to_face_10_photo(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        
        if user.tg_id in [6424595615, 1066043357]:
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
                keyboard.add(InlineKeyboardButton(text=button.text, callback_data=f'{button.data} {button.text}'))

            bot.send_message(user.tg_id, text, reply_markup=keyboard)



    def face_to_face_10_photo_input(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
        user - {user}
        call_data - {callback_data}
        call_id - {callback_id}
        message - {message}''')

        if user.tg_id in [6424595615, 1066043357]:
            
            user.state = state.current_state
            user.save()

            try:
                # Получаем все фото из сообщения
                photos = []
                if 'photo' in message:
                    # Собираем все уникальные file_id фотографий
                    seen_file_ids = set()
                    for photo_sizes in message['photo']:
                        file_id = photo_sizes['file_id']
                        if file_id not in seen_file_ids:
                            seen_file_ids.add(file_id)
                            # Берём только самое большое разрешение для каждого фото
                            photos.append(max(
                                [p for p in message['photo'] if p['file_id'] == file_id],
                                key=lambda x: x['file_size']
                            )['file_id'])
                else:
                    raise ValueError("В сообщении отсутствуют фото")

                # Ограничиваем количество фото до 10
                photos = photos[:10]
                total_photos = len(photos)
                
                # Отправляем информационное сообщение
                bot.send_message(user.tg_id, f"Начинаю обработку {total_photos} фотографий...")

                # Последовательно обрабатываем каждое фото
                for idx, file_id in enumerate(photos, 1):
                    try:
                        # Получаем информацию о файле
                        file_info = bot.get_file(file_id)
                        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'

                        # Загружаем фото
                        response = requests.get(file_url, stream=True)
                        if response.status_code == 200:
                            # Создаём уникальное имя файла
                            file_name = f"user_photo_leonardo_{user.id}_{int(time.time())}_{idx}.jpg"
                            file_path = f'/root/project/bot_bulder/bot_builder/media/{file_name}'
                            
                            # Сохраняем локально
                            with open(file_path, 'wb') as f:
                                f.write(response.content)

                            # Отправляем на сервер
                            try:
                                with open(file_path, 'rb') as f, open(user.photo.path, 'rb') as user_photo:
                                    files = {
                                        'photo': f,
                                        'user_photo': user_photo
                                    }
                                    data = {
                                        'user_id': user.tg_id,
                                        'prompt': f'generation_10_photo {user.summa}_{user.period}_{user.interes}_{user.type_investor}_{user.gender}_{user.format_photo}',
                                    }
                                    
                                    response = requests.post('http://91.218.245.239:8091/create_task', 
                                                        data=data, 
                                                        files=files,
                                                        timeout=30)  # Добавляем timeout
                                    
                                    if response.status_code == 200:
                                        print(f"Фото {idx}/{total_photos} успешно обработано: ", response.json())
                                        bot.send_message(user.tg_id, f"✅ Фото {idx}/{total_photos} успешно обработано")
                                    else:
                                        bot.send_message(user.tg_id, 
                                                    f"❌ Не удалось обработать фото {idx}/{total_photos}. "
                                                    f"Код ответа: {response.status_code}")

                            except requests.exceptions.RequestException as e:
                                print(f"Ошибка при отправке запроса: {e}")
                                bot.send_message(user.tg_id, f"❌ Ошибка при отправке фото {idx}/{total_photos} на сервер")
                            
                            finally:
                                # Удаляем временный файл
                                try:
                                    os.remove(file_path)
                                except Exception as e:
                                    print(f"Ошибка при удалении временного файла: {e}")

                            # Делаем небольшую паузу между запросами
                            time.sleep(1)

                    except Exception as e:
                        print(f"Ошибка при обработке фото {idx}/{total_photos}: {e}")
                        bot.send_message(user.tg_id, f"❌ Ошибка при обработке фото {idx}/{total_photos}: {str(e)}")
                        continue

                # Отправляем сообщение о завершении обработки
                bot.send_message(user.tg_id, f"✅ Обработка всех {total_photos} фотографий завершена!")

            except Exception as e:
                error_message = f"❌ Общая ошибка: {str(e)}"
                print(error_message)
                bot.send_message(user.tg_id, error_message)
                return

            # Добавляем базовые переменные
            self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
            self.val['user_id'] = user.tg_id
            self.val['text'] = 'Базовое сообщение'

            # Форматируем текст с использованием переменных
            text = self.format_message_text(state.text)

            # Создаём кнопки
            buttons = Bot_Button.objects.filter(message_trigger=state)
            keyboard = InlineKeyboardMarkup()
            for button in buttons:
                keyboard.add(InlineKeyboardButton(
                    text=button.text,
                    callback_data=f'{button.data} {button.text}'
                ))

            bot.send_message(user.tg_id, text, reply_markup=keyboard)



    def status_server(self, bot, state, user, callback_data, callback_id, message, event):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        if user.tg_id in [6424595615, 1066043357]:
            user.state = state.current_state
            user.save()

            # Добавляем базовые переменные

            response = requests.get('http://91.218.245.239:8091/user_waiting', stream=True)
            if response.status_code == 200:
                data = response.json()
                
                # Формируем основной текст
                formatted_text = (
                    f"Очередь ожидания: {data['user_waiting']}\n"
                    f"Принятых генераций: {data['procces_accepted']}\n"
                    f"Завершенных генераций: {data['proccess_completed']}\n"
                    f"Генераций с ошибкой: {data['proccess_error']}\n"
                    f"Информация о серверах:\n"
                )
                
                # Обрабатываем серверы
                server_info = ""
                for key, value in data.items():
                    if key.startswith("server_"):  # Считаем ключи, начинающиеся с "server_"
                        server_info += f"  {key.replace('server_', 'Сервер ')}: {value}%\n"

                # Добавляем информацию о серверах в основной текст
                formatted_text += server_info
                
                # Сохраняем результат в self.val['response']
                self.val['response'] = formatted_text


            # Форматируем текст с использованием переменных
            text = self.format_message_text(state.text)

            buttons = Bot_Button.objects.filter(message_trigger=state)
            keyboard = InlineKeyboardMarkup()
            for button in buttons:
                keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

            bot.send_message(user.tg_id, text, reply_markup=keyboard)
