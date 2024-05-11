from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Adresses, Post


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id','first_name', 'last_name', 'role', 'post', 'adress')
    list_display_links = ('first_name', 'last_name', )
    # ordering = ['opened_date', 'title']
    list_per_page = 10

    list_filter = ['role']


@admin.register(Adresses)
class AdressesAdmin(admin.ModelAdmin):
    list_display = ('adress',)
    list_display_links = ('adress',)
    ordering = ['adress', ]
    list_per_page = 10


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post',)
    list_display_links = ('post',)
    ordering = ['post', ]
    list_per_page = 10
