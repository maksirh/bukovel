from datetime import date, timedelta

from django.core import mail
from django.core.cache import cache
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.bookings.forms import BookingForm
from apps.bookings.models import BookingRequest
from apps.offers.models import SpecialOffer
from apps.offers.querysets import active_offers
from apps.rooms.models import RoomType


class BookingFormTests(TestCase):
    def setUp(self):
        self.room = RoomType.objects.create(
            slug='standard',
            title='Standard',
            is_active=True,
        )

    def test_valid_form(self):
        form = BookingForm(data={
            'full_name': 'Test User',
            'phone': '+380501234567',
            'email': 'test@example.com',
            'check_in': date.today() + timedelta(days=1),
            'check_out': date.today() + timedelta(days=3),
            'adults': 2,
            'children': 0,
            'room_type': self.room.pk,
            'message': '',
        })
        self.assertTrue(form.is_valid())

    def test_check_out_must_be_after_check_in(self):
        form = BookingForm(data={
            'full_name': 'Test User',
            'phone': '+380501234567',
            'email': '',
            'check_in': date.today() + timedelta(days=3),
            'check_out': date.today() + timedelta(days=1),
            'adults': 2,
            'children': 0,
            'message': '',
        })
        self.assertFalse(form.is_valid())

    def test_invalid_phone(self):
        form = BookingForm(data={
            'full_name': 'Test User',
            'phone': 'abc',
            'email': '',
            'check_in': date.today() + timedelta(days=1),
            'check_out': date.today() + timedelta(days=3),
            'adults': 2,
            'children': 0,
            'message': '',
        })
        self.assertFalse(form.is_valid())


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    BOOKING_NOTIFY_EMAIL='bookings@example.com',
)
class BookingSubmitViewTests(TestCase):
    def setUp(self):
        cache.clear()
        self.url = reverse('booking_submit')
        self.valid_data = {
            'full_name': 'Test User',
            'phone': '+380501234567',
            'email': 'guest@example.com',
            'check_in': (date.today() + timedelta(days=1)).isoformat(),
            'check_out': (date.today() + timedelta(days=3)).isoformat(),
            'adults': 2,
            'children': 0,
            'message': 'Late check-in',
            'result_id': 'booking-result',
        }

    def test_successful_booking_sends_single_email(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookingRequest.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_invalid_form_returns_errors(self):
        data = {**self.valid_data, 'phone': 'bad'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BookingRequest.objects.count(), 0)
        self.assertIn('form__error', response.content.decode())

    def test_rate_limit_blocks_excessive_requests(self):
        for _ in range(5):
            self.client.post(self.url, self.valid_data)
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(BookingRequest.objects.count(), 5)
        self.assertIn('form__error', response.content.decode())


class ActiveOffersQuerysetTests(TestCase):
    def test_excludes_expired_offers(self):
        SpecialOffer.objects.create(
            slug='expired',
            title='Expired',
            description='Old',
            valid_to=date.today() - timedelta(days=1),
            is_active=True,
        )
        SpecialOffer.objects.create(
            slug='active',
            title='Active',
            description='Current',
            is_active=True,
        )
        slugs = list(active_offers().values_list('slug', flat=True))
        self.assertIn('active', slugs)
        self.assertNotIn('expired', slugs)
