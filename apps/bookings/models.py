from django.db import models


class BookingRequest(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONTACTED = 'contacted'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (STATUS_NEW, 'Новий'),
        (STATUS_CONTACTED, 'Зв\'язались'),
        (STATUS_CONFIRMED, 'Підтверджено'),
        (STATUS_CANCELLED, 'Скасовано'),
    ]

    full_name = models.CharField("Ім'я та прізвище", max_length=150)
    phone = models.CharField('Телефон', max_length=30)
    email = models.EmailField('Email', blank=True)
    check_in = models.DateField('Дата заїзду')
    check_out = models.DateField('Дата виїзду')
    adults = models.PositiveSmallIntegerField('Дорослих', default=2)
    children = models.PositiveSmallIntegerField('Дітей', default=0)
    room_type = models.ForeignKey(
        'rooms.RoomType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Тип номера',
        related_name='booking_requests',
    )
    message = models.TextField('Побажання', blank=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    created_at = models.DateTimeField('Дата заявки', auto_now_add=True)
    ip_address = models.GenericIPAddressField('IP-адреса', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заявка на бронювання'
        verbose_name_plural = 'Заявки на бронювання'

    def __str__(self):
        return f'{self.full_name} / {self.check_in} – {self.check_out}'

    @property
    def nights(self):
        if self.check_in and self.check_out:
            return (self.check_out - self.check_in).days
        return 0
