from django.db import models
from django.urls import reverse


class SpecialOffer(models.Model):
    slug = models.SlugField('Slug', unique=True)
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.CharField('Підзаголовок', max_length=300, blank=True)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='offers/', blank=True)
    discount_percent = models.PositiveSmallIntegerField('Знижка, %', default=0)
    valid_from = models.DateField('Дійсна з', null=True, blank=True)
    valid_to = models.DateField('Дійсна до', null=True, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Спецпропозиція'
        verbose_name_plural = 'Спецпропозиції'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('offer_detail', kwargs={'slug': self.slug})
