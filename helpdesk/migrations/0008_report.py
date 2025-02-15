# Generated by Django 5.0.1 on 2024-02-06 12:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0007_remove_ticket_files_ticket_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('speed', models.CharField(choices=[('быстро', 'Быстро'), ('пришлось подождать', 'Пришлось подождать'), ('очень долго', 'Очень долго')], default='быстро', max_length=50, verbose_name='Скорость')),
                ('feedback', models.TextField(blank=True, verbose_name='Отзыв')),
                ('decision', models.CharField(choices=[('проблема решилась сама', 'Проблема решилась сама'), ('проблему решил сотрудник', 'Проблему решил сотрудник'), ('самостоятельное решение', 'Самостоятельное решение')], default='проблему решил сотрудник', max_length=50, verbose_name='Решение')),
                ('empl_evaluation', models.IntegerField(blank=True, null=True, verbose_name='Оценка сотрудника')),
                ('empl', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='empl_reports', to=settings.AUTH_USER_MODEL)),
                ('ticket', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reports', to='helpdesk.ticket')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_reports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
