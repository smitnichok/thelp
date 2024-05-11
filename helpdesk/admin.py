from django.contrib import admin

from helpdesk.models import Ticket, Equipment


# Register your models here.
@admin.register(Ticket)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ('title', 'equipment', 'status', 'priority', 'type', 'opened_date',  'closed_date' )
    list_display_links = ('title', )
    ordering = ['opened_date', 'title']
    list_per_page = 10
    search_fields = ['title', 'status']
    list_filter = ['status', 'type']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name_equipment',)
    list_display_links = ('name_equipment', )
    ordering = ['name_equipment']
    list_per_page = 10



