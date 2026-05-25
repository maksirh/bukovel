from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from .forms import BookingForm
from .models import BookingRequest
from .utils import get_client_ip, increment_booking_rate_limit, is_booking_rate_limited


def booking_page(request):
    room_pk = request.GET.get('room')
    form = BookingForm(room_type_pk=room_pk)
    return render(request, 'bookings/form.html', {'form': form})


def booking_modal(request):
    room_pk = request.GET.get('room')
    form = BookingForm(room_type_pk=room_pk)
    return render(request, 'bookings/_modal_form.html', {'form': form})


@require_POST
def booking_submit(request):
    result_id = request.POST.get('result_id', 'booking-result')

    if is_booking_rate_limited(request):
        form = BookingForm(request.POST)
        form.add_error(None, _('Too many requests. Please try again in an hour.'))
        return render(request, 'bookings/_error.html', {'form': form, 'result_id': result_id})

    form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.ip_address = get_client_ip(request)
        booking.save()
        increment_booking_rate_limit(request)
        _send_booking_email(booking, request)
        return render(request, 'bookings/_success.html', {'booking': booking, 'result_id': result_id})
    return render(request, 'bookings/_error.html', {'form': form, 'result_id': result_id})


def _send_booking_email(booking: BookingRequest, request):
    subject = f'Нова заявка на бронювання від {booking.full_name}'
    body = render_to_string('bookings/_email_notify.txt', {'booking': booking, 'request': request})
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.BOOKING_NOTIFY_EMAIL],
            fail_silently=True,
        )
    except Exception:
        pass
