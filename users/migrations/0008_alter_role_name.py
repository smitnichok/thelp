# Generated by Django 5.0.1 on 2024-02-17 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_post_alter_user_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=100, verbose_name='роль'),
        ),
    ]
