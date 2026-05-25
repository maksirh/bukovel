from django.contrib import admin
from django.utils.html import format_html
from modeltranslation.admin import TranslationAdmin
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django import forms

from .models import SpecialOffer


class SpecialOfferForm(forms.ModelForm):
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
        model = SpecialOffer
        fields = '__all__'


@admin.register(SpecialOffer)
class SpecialOfferAdmin(TranslationAdmin, ModelAdmin):
    form = SpecialOfferForm
    list_display = ('offer_preview', 'title', 'discount_percent', 'valid_from', 'valid_to', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('offer_preview', 'title')
    prepopulated_fields = {'slug': ('title_uk',)}
    readonly_fields = ('offer_preview',)

    fieldsets = (
        ('Параметри акції', {
            'fields': ('slug', 'discount_percent', ('valid_from', 'valid_to'), 'order', 'is_active'),
            'description': 'Залиште дати порожніми, якщо акція безстрокова',
        }),
        ('Зображення', {
            'fields': (('image', 'offer_preview'),),
        }),
        ('Заголовок та опис — Українська', {
            'fields': ('title_uk', 'subtitle_uk', 'description_uk'),
        }),
        ('Title & description — English', {
            'fields': ('title_en', 'subtitle_en', 'description_en'),
            'classes': ('collapse',),
        }),
    )

    def offer_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height:60px;border-radius:4px">', obj.image.url)
        return '—'
    offer_preview.short_description = 'Фото'
