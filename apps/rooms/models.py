from django.db import models
from django.urls import reverse


class RoomType(models.Model):
    slug = models.SlugField('Slug', unique=True)
    title = models.CharField('Назва', max_length=150)
    area_m2 = models.PositiveSmallIntegerField('Площа, м²', default=30)
    max_guests = models.PositiveSmallIntegerField('Макс. гостей', default=2)
    beds = models.CharField('Ліжка', max_length=100, blank=True)
    rooms_count = models.PositiveSmallIntegerField('Кількість кімнат', default=1)
    short_description = models.TextField('Короткий опис', blank=True)
    description = models.TextField('Повний опис', blank=True)
    base_price = models.DecimalField('Ціна від, грн/ніч', max_digits=10, decimal_places=0, default=0)
    cover_image = models.ImageField('Обкладинка', upload_to='rooms/', blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Тип номера'
        verbose_name_plural = 'Типи номерів'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('room_detail', kwargs={'slug': self.slug})


class RoomImage(models.Model):
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Тип номера',
    )
    image = models.ImageField('Зображення', upload_to='rooms/gallery/')
    alt = models.CharField('Alt-текст', max_length=150, blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Зображення номера'
        verbose_name_plural = 'Зображення номера'

    def __str__(self):
        return f'{self.room_type.title} — фото {self.order}'


class RoomFeature(models.Model):
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='Тип номера',
    )
    icon = models.CharField('Іконка (emoji або назва)', max_length=50, blank=True)
    title = models.CharField('Назва фічі', max_length=100)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Особливість номера'
        verbose_name_plural = 'Особливості номера'

    def __str__(self):
        return f'{self.room_type.title} — {self.title}'
