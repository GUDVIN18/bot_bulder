# Generated by Django 5.1.1 on 2024-09-26 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_bot_message_next_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot_message',
            name='next_state',
            field=models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Ссылка на состояние при вводе'),
        ),
    ]
