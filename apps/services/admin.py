from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django import forms

from .models import Service


class ServiceForm(forms.ModelForm):
    description_uk = forms.CharField(
        label='Повний опис — Українська',
        widget=TinyMCE(),
        required=False,
    )
    description_en = forms.CharField(
        label='Full description — English',
        widget=TinyMCE(),
        required=False,
    )

    class Meta:
        model = Service
        fields = '__all__'


@admin.register(Service)
class ServiceAdmin(TranslationAdmin, ModelAdmin):
    form = ServiceForm
    list_display = ('service_preview', 'title', 'icon', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('service_preview', 'title')
    prepopulated_fields = {'slug': ('title_uk',)}
    readonly_fields = ('service_preview',)

    fieldsets = (
        ('Основне', {
            'fields': ('slug', 'icon', 'order', 'is_active'),
        }),
        ('Назва та описи — Українська', {
            'fields': ('title_uk', 'short_description_uk', 'description_uk'),
            'description': 'Короткий опис — для картки на головній; повний — для окремої сторінки послуги',
        }),
        ('Title & descriptions — English', {
            'fields': ('title_en', 'short_description_en', 'description_en'),
            'classes': ('collapse',),
        }),
        ('Зображення', {
            'fields': (('image', 'service_preview'),),
        }),
    )

    def service_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;border-radius:4px">', obj.image.url)
        return '—'
    service_preview.short_description = 'Фото'
