# Generated by Django 5.0.1 on 2024-02-17 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0012_alter_ticket_closed_date_alter_ticket_opened_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'verbose_name': 'заявку', 'verbose_name_plural': 'заявки'},
        ),
    ]
