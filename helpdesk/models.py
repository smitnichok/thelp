from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from users.models import User


class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('активная', 'Активная',),
        ('в процессе', 'В процессе',),
        ('выполнено', 'Выполнено',),)

    TYPE_CHOICES = (
        ('неожиданная проблема', 'Неожиданная проблема',),
        ('повторное обращение', 'Повторное обращение',),
        ('консультация', 'Kонсультация',),)

    PRIORITY_CHOICES = (
        ('низкий', 'Низкий',),
        ('средний', 'Средний',),
        ('высокий', 'Высокий',),)

    title = models.CharField(max_length=50, verbose_name="Тема")
    equipment = models.ForeignKey('Equipment', on_delete=models.PROTECT, related_name='equipment', default='монитор',
                                  verbose_name="оборудование")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='активная', verbose_name="статус")
    description = models.TextField(blank=True, verbose_name="описание")
    type = models.CharField(max_length=40, choices=TYPE_CHOICES, default='неожиданная проблема',
                            verbose_name="Тип обращения")
    priority = models.CharField(max_length=40, choices=PRIORITY_CHOICES, default='cредний', verbose_name="Приоритет")

    opened_date = models.DateTimeField(auto_now_add=True, verbose_name="открыто")
    closed_date = models.DateTimeField(blank=True, null=True, verbose_name="выполнено")
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='ticket', null=True,
                             default=None)
    empl = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='empl', null=True, blank=True)


    class Meta:
        verbose_name = "заявку"
        verbose_name_plural = "заявки"

    def get_absolute_url(self):
        return reverse('my_ticket_detail', args=[self.id])

    def __str__(self):
        return f"Ticket ID: {self.id} - {self.title} ({self.status})"


class Equipment(models.Model):
    name_equipment = models.CharField(max_length=60, verbose_name="оборудование")

    class Meta:
        verbose_name = "Оборудование/ПО"
        verbose_name_plural = "Оборудование"

    def __str__(self):
        return self.name_equipment


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')


5