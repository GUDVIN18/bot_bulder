from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    fields = [
        "user",
        "status",
        'update_data',
    ]
    list_display = (
        "user",
        "status",
    )
    list_filter = (
        "user",
        "status",
    )
    search_fields = (
        "user",
        "status",
    )
