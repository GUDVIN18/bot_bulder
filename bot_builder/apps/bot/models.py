from django.db import models


class TelegramBotConfig(models.Model):
    bot_token = models.CharField(max_length=100)
    is_activ = models.BooleanField(null=False, blank=False, default=False, verbose_name="Is active")

    def __str__(self):
        return f'{self.bot_token}'

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"





class BotUser(models.Model):
    tg_id = models.BigIntegerField(unique=True, verbose_name="ID Telegram")
    first_name = models.CharField(max_length=250, verbose_name="Имя пользователя", blank=True, null=True)
    last_name = models.CharField(max_length=250, verbose_name="Фамилия пользователя", blank=True, null=True)
    username = models.CharField(max_length=250, verbose_name="Username пользователя", blank=True, null=True)
    language = models.CharField(max_length=250, verbose_name="Язык пользователя", blank=True, null=True)
    premium = models.BooleanField(verbose_name="Имеет ли пользователь премиум-аккаунт", default=False, blank=True, null=True)
    # state = models.CharField(max_length=110, choices=STATE_CHOICES, default='')
    state = models.CharField(max_length=255, help_text='Состояние')


    def __str__(self):
        return f"user_object {self.tg_id} {self.username}"

    class Meta:
        verbose_name = "Пользователь бота"
        verbose_name_plural = "Пользователи бота"






class Bot_Message(models.Model):
    text = models.TextField(verbose_name="Текст сообщения")
    current_state =  models.CharField(max_length=110, verbose_name="К какому состоянию привязана?", default=None, unique=True)
    next_state = models.CharField(max_length=255, verbose_name="Ссылка на состояние при вводе", default=None, null=True, blank=True)
    handler = models.CharField(max_length=255, verbose_name="Имя функции обработчика", null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.text[:50]}... (Состояние: {self.current_state})"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"



class Bot_Commands(models.Model):
    text = models.CharField(max_length=255, verbose_name="Текст команды")
    trigger = models.ForeignKey(Bot_Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='triggered_commands', verbose_name="Связанное сообщение")

    def __str__(self):
        return f"{self.text} (Триггер: {self.trigger})"

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"



class Bot_Button(models.Model):
    text = models.CharField(max_length=255, verbose_name="Текст кнопки")
    message_trigger = models.ForeignKey(Bot_Message, on_delete=models.SET_NULL, null=True, blank=True, related_name='message_triggered', verbose_name="Связанное сообщение")
    data = models.CharField(max_length=255, verbose_name='Данные', default='')

    def __str__(self):
        return f"{self.text} (Триггер: {self.message_trigger})"

    class Meta:
        verbose_name = "Кнопку"
        verbose_name_plural = "Кнопки"
