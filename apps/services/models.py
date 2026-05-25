from django.db import models
from django.urls import reverse


class Service(models.Model):
    slug = models.SlugField('Slug', unique=True)
    title = models.CharField('Назва', max_length=150)
    short_description = models.TextField('Короткий опис')
    description = models.TextField('Повний опис', blank=True)
    icon = models.CharField('Іконка (emoji або svg)', max_length=10, blank=True)
    image = models.ImageField('Зображення', upload_to='services/', blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активна', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Послуга'
        verbose_name_plural = 'Послуги'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})
