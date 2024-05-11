from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from django.urls import reverse
from django.utils.text import slugify


def translit_to_eng(s: str) -> str:
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}

    return "".join(d.get(c, c) for c in s.lower())


class Manuals(models.Model):
    title = models.CharField(max_length=255, verbose_name="Тема")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", validators=[
        MinLengthValidator(5, message="Минимум 5 символов"),
        MaxLengthValidator(100, message="Максимум 100 символов"),
    ])

    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фото")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='category', verbose_name="Категории")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True,
                               default=None)

    class Meta:
        verbose_name = "статью"
        verbose_name_plural = "статьи"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(translit_to_eng(self.title))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})
