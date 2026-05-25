from django.shortcuts import render, get_object_or_404
from .models import RoomType
from apps.bookings.forms import BookingForm


def room_list(request):
    rooms = RoomType.objects.filter(is_active=True)
    context = {'rooms': rooms}
    return render(request, 'rooms/list.html', context)


def room_detail(request, slug):
    room = get_object_or_404(RoomType, slug=slug, is_active=True)
    other_rooms = RoomType.objects.filter(is_active=True).exclude(pk=room.pk)[:4]
    booking_form = BookingForm(room_type_pk=room.pk)
    context = {
        'room': room,
        'other_rooms': other_rooms,
        'booking_form': booking_form,
    }
    return render(request, 'rooms/detail.html', context)
