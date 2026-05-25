from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from unfold.admin import ModelAdmin, TabularInline
from tinymce.widgets import TinyMCE
from django import forms

from .models import RoomType, RoomImage, RoomFeature


@admin.register(RoomImage)
class RoomImageAdmin(ModelAdmin):
    list_display = ('image_preview', 'room_type', 'alt', 'order')
    list_editable = ('order',)
    list_filter = ('room_type',)
    list_display_links = ('image_preview', 'room_type')
    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Фото', {
            'fields': (('image', 'image_preview'), 'alt', 'order', 'room_type'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px">', obj.image.url)
        return '—'
    image_preview.short_description = 'Фото'


class RoomTypeForm(forms.ModelForm):
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
        model = RoomType
        fields = '__all__'


class RoomImageInline(TabularInline):
    model = RoomImage
    extra = 2
    fields = ('image', 'image_preview', 'alt', 'order')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px">', obj.image.url)
        return '—'
    image_preview.short_description = 'Прев\'ю'


class RoomFeatureInline(TranslationTabularInline, TabularInline):
    model = RoomFeature
    extra = 2
    fields = ('icon', 'title_uk', 'title_en', 'order')


@admin.register(RoomType)
class RoomTypeAdmin(TranslationAdmin, ModelAdmin):
    form = RoomTypeForm
    list_display = ('cover_preview', 'title', 'area_m2', 'max_guests', 'base_price', 'order', 'is_active')
    list_editable = ('order', 'is_active', 'base_price')
    list_display_links = ('cover_preview', 'title')
    prepopulated_fields = {'slug': ('title_uk',)}
    inlines = [RoomImageInline, RoomFeatureInline]
    readonly_fields = ('cover_preview',)

    fieldsets = (
        ('Основне', {
            'fields': ('slug', ('cover_image', 'cover_preview'), 'order', 'is_active'),
        }),
        ('Характеристики', {
            'fields': ('area_m2', 'max_guests', 'beds_uk', 'rooms_count', 'base_price'),
        }),
        ('Beds — English', {
            'fields': ('beds_en',),
            'classes': ('collapse',),
        }),
        ('Назва та опис — Українська', {
            'fields': ('title_uk', 'short_description_uk', 'description_uk'),
        }),
        ('Title & description — English', {
            'fields': ('title_en', 'short_description_en', 'description_en'),
            'classes': ('collapse',),
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:50px;border-radius:4px">', obj.cover_image.url)
        return '—'
    cover_preview.short_description = 'Фото'
