from django.db import models

from apps.core.models import SingletonModel


class RestaurantInfo(SingletonModel):
    title = models.CharField('Назва', max_length=150, default='Ресторан м\'яса та вина')
    description = models.TextField('Опис', blank=True)
    opening_hours = models.CharField('Години роботи', max_length=50, default='13:00 – 23:00')
    breakfast_hours = models.CharField('Сніданки', max_length=50, default='08:00 – 11:00')
    cover_image = models.ImageField('Обкладинка', upload_to='restaurant/', blank=True)

    class Meta:
        verbose_name = 'Інфо про ресторан'
        verbose_name_plural = 'Інфо про ресторан'

    def __str__(self):
        return self.title


class MenuSection(models.Model):
    title = models.CharField('Назва розділу', max_length=150)
    description = models.TextField('Опис', blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Розділ меню'
        verbose_name_plural = 'Розділи меню'

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    section = models.ForeignKey(
        MenuSection,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Розділ',
    )
    title = models.CharField('Назва', max_length=200)
    description = models.TextField('Опис', blank=True)
    price = models.DecimalField('Ціна, грн', max_digits=8, decimal_places=0, default=0)
    image = models.ImageField('Фото', upload_to='restaurant/menu/', blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Позиція меню'
        verbose_name_plural = 'Позиції меню'

    def __str__(self):
        return self.title


class RestaurantPhoto(models.Model):
    image = models.ImageField('Фото', upload_to='restaurant/gallery/')
    alt = models.CharField('Підпис (alt)', max_length=200, blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Фото галереї'
        verbose_name_plural = 'Фото галереї'

    def __str__(self):
        return self.alt or f'Фото {self.pk}'
