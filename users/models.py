from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=100, verbose_name='роль')

    def __str__(self):
        return self.name


class Adresses(models.Model):
    adress = models.CharField(max_length=150)

    class Meta:
        verbose_name = "адрес"
        verbose_name_plural = "адреса"

    def __str__(self):
        return self.adress


class Post(models.Model):
    post = models.CharField(max_length=100)

    class Meta:
        verbose_name = "должность"
        verbose_name_plural = "должности"

    def __str__(self):
        return self.post


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users', blank=True, null=True,
                             verbose_name='роль')
    patronymic = models.CharField(max_length=60, blank=True, null=True, verbose_name='отчество')
    post = models.ForeignKey('Post', on_delete=models.PROTECT, blank=True, null=True, related_name='posts',
                             verbose_name="должность")
    cabinet = models.IntegerField(null=True, blank=True, verbose_name="кабинет")
    number_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='номер телефона')
    adress = models.ForeignKey('Adresses', on_delete=models.PROTECT, blank=True, null=True, related_name='adresses',
                               verbose_name="адрес")
    image = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None, blank=True, null=True, verbose_name="фото")
