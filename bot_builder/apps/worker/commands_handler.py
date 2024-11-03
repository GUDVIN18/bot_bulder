from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from apps.bot.models import Bot_Message, Bot_Button, BotUser
import requests
from datetime import datetime

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




    def base(self, bot, state, user, callback_data, callback_id, message):
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




    def start(self, bot, state, user, callback_data, callback_id, message):
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




    def weather(self, bot, state, user, callback_data, callback_id, message):
        self.val = {}  # Очищаем переменные
        user.state = state.current_state
        user.save()

        print(f'''------------- weather 
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')


        try:
            weather_message = Bot_Message.objects.get(current_state='weather')
            text = self.format_message_text(weather_message.text)
        except Bot_Message.DoesNotExist:
            text = "Ошибка при получении состояния def weather()"

        buttons = Bot_Button.objects.filter(message_trigger=weather_message)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)

    def Moskow(self, bot, state, user, callback_data, callback_id, message):
        self.val = {}  # Очищаем переменные
        user.state = state.current_state
        user.save()
        city_id_dict = {'moskow': 524901}

        api_key = 'c42fb5f8d37ff5c951a9628a751e27c8'
        city_id = city_id_dict[callback_data.split(' ')[1]]

        url = f'http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric'
        
        try:
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                # Сохраняем все доступные данные в переменные
                self.val['temperature'] = round(data['main']['temp'], 1)
                self.val['description'] = data['weather'][0]['description']
                self.val['humidity'] = data['main']['humidity']
                self.val['pressure'] = data['main']['pressure']
                self.val['wind_speed'] = data['wind']['speed']
                self.val['city_name'] = 'Москва'
                self.val['current_time'] = datetime.now().strftime('%H:%M')
                self.val['date'] = datetime.now().strftime('%Y-%m-%d')
                self.val['feels_like'] = round(data['main']['feels_like'], 1)
            else:
                self.val['error'] = f"Ошибка при получении данных: {data['message']}"
        
        except requests.RequestException as e:
            self.val['error'] = f"Ошибка при выполнении запроса: {e}"

        try:
            moscow_message = Bot_Message.objects.get(current_state='Moskow')
            text = self.format_message_text(moscow_message.text)
        except Bot_Message.DoesNotExist:
            text = "Ошибка при получении состояния def Moskow()"

        buttons = Bot_Button.objects.filter(message_trigger=moscow_message)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)






    def select_an_item(self, bot, state, user, callback_data, callback_id, message):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        
        print(f'\n\n\n user.state до {user.state}\nпосле {state.current_state} ')

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






    #Обработка текста пользователя
    def text_processing(self, bot, state, user, callback_data, callback_id, message):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        
        print(f'\n\n\n user.state до {user.state}\nпосле {state.current_state} ')

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



    #Обработка текста пользователя comlete
    def text_processing_complete(self, bot, state, user, callback_data, callback_id, message):
        self.val = {}  # Очищаем переменные для каждого нового вызова
        print(f'''
            user - {user}
            call_data - {callback_data}
            call_id - {callback_id}
            message - {message}''')
        
        
        print(f'\n\n\n user.state до {user.state}\nпосле {state.current_state} ')

        user.state = state.current_state
        user.save()

        # Добавляем базовые переменные
        self.val['user_name'] = user.name if hasattr(user, 'name') else 'Пользователь'
        self.val['user_id'] = user.tg_id
        self.val['text'] = message['text']  # Значение по умолчанию

        # Форматируем текст с использованием переменных
        text = self.format_message_text(state.text)

        buttons = Bot_Button.objects.filter(message_trigger=state)
        keyboard = InlineKeyboardMarkup()
        for button in buttons:
            keyboard.add(InlineKeyboardButton(text=button.text, callback_data=button.data))

        bot.send_message(user.tg_id, text, reply_markup=keyboard)