import re

from django import forms
from django.utils.translation import gettext_lazy as _

from apps.rooms.models import RoomType

from .models import BookingRequest

PHONE_RE = re.compile(r'^\+?[0-9\s\-()]{10,20}$')


class BookingForm(forms.ModelForm):
    check_in = forms.DateField(
        label='Дата заїзду',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
    )
    check_out = forms.DateField(
        label='Дата виїзду',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}),
    )

    class Meta:
        model = BookingRequest
        fields = ['full_name', 'phone', 'email', 'check_in', 'check_out',
                  'adults', 'children', 'room_type', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form__input', 'placeholder': "Ваше ім'я"}),
            'phone': forms.TextInput(attrs={'class': 'form__input', 'placeholder': '+380...', 'type': 'tel'}),
            'email': forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'email@example.com'}),
            'adults': forms.NumberInput(attrs={'class': 'form__input form__input--small', 'min': 1, 'max': 10}),
            'children': forms.NumberInput(attrs={'class': 'form__input form__input--small', 'min': 0, 'max': 8}),
            'room_type': forms.Select(attrs={'class': 'form__select'}),
            'message': forms.Textarea(attrs={'class': 'form__textarea', 'rows': 3, 'placeholder': 'Побажання або запитання...'}),
        }

    def __init__(self, *args, room_type_pk=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['room_type'].queryset = RoomType.objects.filter(is_active=True)
        self.fields['room_type'].empty_label = '— Оберіть номер —'
        self.fields['room_type'].required = False
        if room_type_pk:
            try:
                self.fields['room_type'].initial = RoomType.objects.get(pk=room_type_pk)
            except RoomType.DoesNotExist:
                pass

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not PHONE_RE.match(phone):
            raise forms.ValidationError(_('Enter a valid phone number.'))
        return phone

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get('check_in')
        check_out = cleaned.get('check_out')
        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError(_('Check-out date must be after check-in date.'))
        return cleaned
