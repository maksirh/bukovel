from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django import forms

from .models import RestaurantInfo, MenuSection, MenuItem, RestaurantPhoto


class RestaurantInfoForm(forms.ModelForm):
    description_uk = forms.CharField(
        label='Опис — Українська',
        widget=TinyMCE(),
        required=False,
    )
    description_en = forms.CharField(
        label='Description — English',
        widget=TinyMCE(),
        required=False,
    )

    class Meta:
        model = RestaurantInfo
        fields = '__all__'



@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(TranslationAdmin, ModelAdmin):
    form = RestaurantInfoForm
    readonly_fields = ('cover_preview',)

    fieldsets = (
        ('Назва та опис — Українська', {
            'fields': ('title_uk', 'description_uk'),
        }),
        ('Title & description — English', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',),
        }),
        ('Години роботи (однакові для всіх мов)', {
            'fields': ('opening_hours', 'breakfast_hours'),
        }),
        ('Обкладинка', {
            'fields': (('cover_image', 'cover_preview'),),
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:100px;border-radius:4px">', obj.cover_image.url)
        return '—'
    cover_preview.short_description = 'Прев\'ю'

    def changelist_view(self, request, extra_context=None):
        obj = RestaurantInfo.load()
        return HttpResponseRedirect(
            reverse('admin:restaurant_restaurantinfo_change', args=[obj.pk])
        )

    def has_add_permission(self, request):
        return not RestaurantInfo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(MenuSection)
class MenuSectionAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)

    fieldsets = (
        ('Порядок', {
            'fields': ('order',),
        }),
        ('Назва та опис — Українська', {
            'fields': ('title_uk', 'description_uk'),
            'description': 'Розділи меню — наприклад: Закуски, Основні страви, Напої',
        }),
        ('Title & description — English', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',),
        }),
    )


@admin.register(MenuItem)
class MenuItemAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('item_preview', 'title', 'section', 'price', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'price')
    list_display_links = ('item_preview', 'title')
    list_filter = ('section', 'is_active')
    readonly_fields = ('item_preview',)

    fieldsets = (
        ('Розділ та ціна', {
            'fields': ('section', 'price', 'order', 'is_active'),
        }),
        ('Назва та опис — Українська', {
            'fields': ('title_uk', 'description_uk'),
        }),
        ('Title & description — English', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',),
        }),
        ('Фото', {
            'fields': (('image', 'item_preview'),),
        }),
    )

    def item_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;border-radius:4px">', obj.image.url)
        return '—'
    item_preview.short_description = 'Фото'


@admin.register(RestaurantPhoto)
class RestaurantPhotoAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('photo_preview', 'alt', 'order')
    list_editable = ('order',)
    list_display_links = ('photo_preview', 'alt')
    readonly_fields = ('photo_preview',)

    fieldsets = (
        ('Порядок', {
            'fields': ('order',),
        }),
        ('Фото', {
            'fields': (('image', 'photo_preview'),),
        }),
        ('Підпис — Українська', {
            'fields': ('alt_uk',),
        }),
        ('Alt — English', {
            'fields': ('alt_en',),
            'classes': ('collapse',),
        }),
    )

    def photo_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px">', obj.image.url)
        return '—'
    photo_preview.short_description = 'Прев\'ю'
