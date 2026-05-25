from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django import forms

from .models import SpaZone, SpaSchedule, SpaPackage, SpaGallery


class SpaZoneForm(forms.ModelForm):
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
        model = SpaZone
        fields = '__all__'


class SpaScheduleForm(forms.ModelForm):
    description_uk = forms.CharField(
        label='Загальний опис SPA — Українська',
        widget=TinyMCE(),
        required=False,
    )
    description_en = forms.CharField(
        label='General SPA description — English',
        widget=TinyMCE(),
        required=False,
    )

    class Meta:
        model = SpaSchedule
        fields = '__all__'


@admin.register(SpaZone)
class SpaZoneAdmin(TranslationAdmin, ModelAdmin):
    form = SpaZoneForm
    list_display = ('zone_preview', 'title', 'order')
    list_editable = ('order',)
    list_display_links = ('zone_preview', 'title')
    prepopulated_fields = {'slug': ('title_uk',)}
    readonly_fields = ('zone_preview',)

    fieldsets = (
        ('Основне', {
            'fields': ('slug', 'order', ('image', 'zone_preview')),
        }),
        ('Назва та опис — Українська', {
            'fields': ('title_uk', 'description_uk'),
        }),
        ('Title & description — English', {
            'fields': ('title_en', 'description_en'),
            'classes': ('collapse',),
        }),
    )

    def zone_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:50px;border-radius:4px">', obj.image.url)
        return '—'
    zone_preview.short_description = 'Фото'


@admin.register(SpaSchedule)
class SpaScheduleAdmin(TranslationAdmin, ModelAdmin):
    form = SpaScheduleForm
    readonly_fields = ('cover_preview',)

    fieldsets = (
        ('Години роботи (однакові для всіх мов)', {
            'fields': ('working_hours', 'sauna_hours'),
            'description': 'Формат: 08:00 – 22:00',
        }),
        ('Опис — Українська', {
            'fields': ('description_uk',),
        }),
        ('Description — English', {
            'fields': ('description_en',),
            'classes': ('collapse',),
        }),
        ('Обкладинка', {
            'fields': (('cover_image', 'cover_preview'),),
        }),
        ('Highlights (іконки під hero)', {
            'fields': (
                ('highlight_1_icon', 'highlight_1_label_uk', 'highlight_1_label_en'),
                ('highlight_2_icon', 'highlight_2_label_uk', 'highlight_2_label_en'),
                ('highlight_3_icon', 'highlight_3_label_uk', 'highlight_3_label_en'),
            ),
            'description': 'Emoji або коротке слово для іконки. Підпис — текст, що показується під іконкою.',
        }),
        ('Блок статистики (цифри)', {
            'fields': (
                ('stat_1_value', 'stat_1_label_uk', 'stat_1_label_en'),
                ('stat_2_value', 'stat_2_label_uk', 'stat_2_label_en'),
                ('stat_3_value', 'stat_3_label_uk', 'stat_3_label_en'),
            ),
            'description': '4-й показник береться автоматично з поля «Години роботи SPA».',
        }),
    )

    def changelist_view(self, request, extra_context=None):
        obj = SpaSchedule.load()
        return HttpResponseRedirect(
            reverse('admin:spa_spaschedule_change', args=[obj.pk])
        )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height:100px;border-radius:4px">', obj.cover_image.url)
        return '—'
    cover_preview.short_description = 'Прев\'ю'

    def has_add_permission(self, request):
        return not SpaSchedule.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class SpaPackageForm(forms.ModelForm):
    features_uk = forms.CharField(
        label='Склад пакету — Українська',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
        help_text='По одному пункту на рядок',
    )
    features_en = forms.CharField(
        label='Package contents — English',
        widget=forms.Textarea(attrs={'rows': 6}),
        required=False,
        help_text='One item per line',
    )

    class Meta:
        model = SpaPackage
        fields = '__all__'


@admin.register(SpaPackage)
class SpaPackageAdmin(TranslationAdmin, ModelAdmin):
    form = SpaPackageForm
    list_display = ('title', 'price', 'duration', 'is_popular', 'order')
    list_editable = ('price', 'is_popular', 'order')
    list_display_links = ('title',)

    fieldsets = (
        ('Основне', {
            'fields': ('order', 'price', 'duration', 'is_popular'),
        }),
        ('Назва та склад — Українська', {
            'fields': ('title_uk', 'features_uk'),
        }),
        ('Title & contents — English', {
            'fields': ('title_en', 'features_en'),
            'classes': ('collapse',),
        }),
    )


@admin.register(SpaGallery)
class SpaGalleryAdmin(TranslationAdmin, ModelAdmin):
    list_display = ('gallery_preview', 'caption', 'order')
    list_editable = ('order',)
    list_display_links = ('gallery_preview', 'caption')
    readonly_fields = ('gallery_preview',)

    fieldsets = (
        ('Фото', {
            'fields': (('image', 'gallery_preview'), 'order'),
        }),
        ('Підпис — Українська', {
            'fields': ('caption_uk',),
        }),
        ('Caption — English', {
            'fields': ('caption_en',),
            'classes': ('collapse',),
        }),
    )

    def gallery_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px">', obj.image.url)
        return '—'
    gallery_preview.short_description = 'Фото'
