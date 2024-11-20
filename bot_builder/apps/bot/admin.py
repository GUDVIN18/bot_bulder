# Register your models here.
from django.contrib import admin
from .models import *




# admin.site.register(FSM_Controller)




@admin.register(TelegramBotConfig)
class TelegramBotConfigAdmin(admin.ModelAdmin):
    fields = [
        "bot_token",
        'is_activ',
    ]
    list_display = (
        "id",
        "bot_token",
        'is_activ',
    )
    list_filter = (
        "bot_token",
        'is_activ',
    )
    search_fields = (
        "bot_token",
    )


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    fields = [
        "tg_id",
        "first_name",
        "last_name",
        "username",
        "language",
        "premium",
        "state",

    ]
    list_display = (
        "tg_id",
        "first_name",
        "username",
        "state",
    )
    list_filter = (
        "tg_id",
        "username",

    )
    search_fields = (
        "tg_id",
        "username",
        "id"
    )




class Bot_ButtonStackedInline(admin.StackedInline):
    model = Bot_Button
    extra = 1
    fields = (
        ('text', 'data',),
    )


@admin.register(Bot_Message)
class Bot_MessageAdmin(admin.ModelAdmin):
    inlines = [Bot_ButtonStackedInline]
    fields = [
        "text",
        "current_state",
        "next_state",
        "anyway_link",
        "handler",
    ]
    list_display = (
        "text", 
        "current_state",
        "next_state",
        "handler",
    )
    list_filter = (
        "handler",
    )
    search_fields = (
        "handler",
    )



@admin.register(Bot_Commands)
class Bot_CommandsAdmin(admin.ModelAdmin):
    fields = [
        "text",
        "trigger",
    ]
    list_display = (
        "text",
        "trigger",
    )
    list_filter = (
        "text",
        "trigger",
    )
    search_fields = (
        "text",
        "trigger",
    )






@admin.register(Bot_Button)
class Bot_ButtonAdmin(admin.ModelAdmin):
    fields = [
        "text",
        "message_trigger",
        "data"
    ]
    list_display = (
        "text",
        "message_trigger",
    )
    list_filter = (
        "text",
        "message_trigger",
    )
    search_fields = (
        "text",
        "message_trigger",
    )
