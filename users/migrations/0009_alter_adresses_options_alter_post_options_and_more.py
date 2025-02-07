# Generated by Django 5.0.1 on 2024-02-17 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_role_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adresses',
            options={'verbose_name': 'адрес', 'verbose_name_plural': 'адреса'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': 'должность', 'verbose_name_plural': 'должности'},
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', to='users.role', verbose_name='роль'),
        ),
    ]
