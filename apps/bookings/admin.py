from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin

from .models import BookingRequest


@admin.register(BookingRequest)
class BookingRequestAdmin(ModelAdmin):
    list_display = ('full_name', 'phone', 'room_type', 'check_in', 'check_out', 'nights_count', 'status', 'created_at')
    list_editable = ('status',)
    list_filter = ('status', 'room_type', 'check_in')
    search_fields = ('full_name', 'phone', 'email')
    date_hierarchy = 'check_in'
    readonly_fields = ('created_at', 'ip_address', 'nights_count')

    fieldsets = (
        ('Гість', {
            'fields': ('full_name', 'phone', 'email'),
        }),
        ('Бронювання', {
            'fields': ('check_in', 'check_out', 'nights_count', 'adults', 'children', 'room_type'),
            'description': 'Кількість ночей розраховується автоматично',
        }),
        ('Деталі', {
            'fields': ('message', 'status', 'created_at', 'ip_address'),
        }),
    )

    def nights_count(self, obj):
        return obj.nights
    nights_count.short_description = 'Ночей'
