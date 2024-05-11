from django.contrib import admin

from empl.models import Manuals, Category


# Register your models here.


@admin.register(Manuals)
class ManulasAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'cat', 'author')
    list_per_page = 10
    search_fields = [ 'author']
    list_filter = ['cat']
    list_display_links = ('title', 'author',)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_per_page = 10
    list_display_links = ('name',)
