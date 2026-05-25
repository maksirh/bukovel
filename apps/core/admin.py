from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django import forms

from .models import SiteSettings, HeroSlide, StatItem


class SiteSettingsForm(forms.ModelForm):
    about_text_uk = forms.CharField(
        label='Текст "Про нас" — Українська',
        widget=TinyMCE(),
        required=False,
    )
    about_text_en = forms.CharField(
        label='Text "About us" — English',
        widget=TinyMCE(),
        required=False,
    )

    class Meta:
        model = SiteSettings
        fields = '__all__'


@admin.register(SiteSettings)
class SiteSettingsAdmin(TranslationAdmin, ModelAdmin):
    form = SiteSettingsForm

    fieldsets = (
        ('Загальне', {
            'fields': ('logo', 'logo_preview', 'logo_white', 'logo_white_preview'),
        }),
        ('Назва та слоган — Українська', {
            'fields': ('site_name_uk', 'tagline_uk'),
        }),
        ('Site name & tagline — English', {
            'fields': ('site_name_en', 'tagline_en'),
            'classes': ('collapse',),
        }),
        ('Контакти', {
            'fields': ('phone', 'phone_secondary', 'email', 'address'),
        }),
        ('Соцмережі', {
            'fields': ('instagram_url', 'facebook_url', 'telegram_url', 'viber_url'),
        }),
        ('Головний екран Hero — Українська', {
            'fields': ('hero_eyebrow_uk', 'hero_video', 'hero_video_poster', 'hero_poster_preview'),
            'description': 'Налаштування першого екрану на головній сторінці',
        }),
        ('Hero screen — English', {
            'fields': ('hero_eyebrow_en',),
            'classes': ('collapse',),
        }),
        ('Про нас — Українська', {
            'fields': ('about_text_uk', 'about_image', 'about_image_preview'),
        }),
        ('About us — English', {
            'fields': ('about_text_en',),
            'classes': ('collapse',),
        }),
        ('Час заїзду / виїзду', {
            'fields': (('check_in_time', 'check_out_time'),),
        }),
        ('Карта Google Maps', {
            'fields': ('map_embed',),
            'description': 'Вставте iframe-код з Google Maps (кнопка "Поділитися → Вставити карту")',
        }),
    )

    readonly_fields = (
        'logo_preview',
        'logo_white_preview',
        'about_image_preview',
        'hero_poster_preview',
    )

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px">', obj.logo.url)
        return '—'
    logo_preview.short_description = 'Прев\'ю'

    def logo_white_preview(self, obj):
        if obj.logo_white:
            return format_html(
                '<img src="{}" style="max-height:60px;border-radius:4px;background:#333;padding:4px">',
                obj.logo_white.url,
            )
        return '—'
    logo_white_preview.short_description = 'Прев\'ю'

    def about_image_preview(self, obj):
        if obj.about_image:
            return format_html('<img src="{}" style="max-height:120px;border-radius:4px">', obj.about_image.url)
        return '—'
    about_image_preview.short_description = 'Прев\'ю'

    def hero_poster_preview(self, obj):
        if obj.hero_video_poster:
            return format_html('<img src="{}" style="max-height:80px;border-radius:4px">', obj.hero_video_poster.url)
        return '—'
    hero_poster_preview.short_description = 'Прев\'ю постера'

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return HttpResponseRedirect(
            reverse('admin:core_sitesettings_change', args=[obj.pk])
        )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('slide_preview', 'title', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)
    readonly_fields = ('slide_preview',)

    fieldsets = (
        ('Зображення та налаштування', {
            'fields': (('image', 'slide_preview'), 'order', 'is_active'),
        }),
        ('Текст — Українська', {
            'fields': ('title_uk', 'subtitle_uk', 'cta_text_uk'),
        }),
        ('Text — English', {
            'fields': ('title_en', 'subtitle_en', 'cta_text_en'),
            'classes': ('collapse',),
        }),
        ('URL кнопки', {
            'fields': ('cta_url',),
            'description': 'Однаковий для обох мов. Наприклад: #booking',
        }),
    )

    def slide_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px">', obj.image.url)
        return '—'
    slide_preview.short_description = 'Прев\'ю'


@admin.register(StatItem)
class StatItemAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('value', 'label', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    ordering = ('order',)

    fieldsets = (
        ('Значення (однакове для всіх мов)', {
            'fields': ('value', 'order', 'is_active'),
            'description': 'Число або символ, наприклад: 22, 5★, 20×8',
        }),
        ('Підпис — Українська', {
            'fields': ('label_uk',),
        }),
        ('Label — English', {
            'fields': ('label_en',),
            'classes': ('collapse',),
        }),
    )
