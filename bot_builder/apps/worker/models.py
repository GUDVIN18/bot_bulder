from django.db import models
from apps.bot.models import BotUser

class Events(models.Model):
    CHOICES = [
        ('ACCEPTED', 'Событие создано'),
        ('COMPLETED', 'Событие закончено'),
    ]
    
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='events', null=True, blank=True)
    status = models.CharField(max_length=110, choices=CHOICES)
    update_data = models.JSONField(verbose_name='JSON объект', default=dict)

    def __str__(self):
        return f"{self.user} {self.status}"

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"