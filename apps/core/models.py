from django.db import models
from django.core.exceptions import ValidationError


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class SiteSettings(SingletonModel):
    site_name = models.CharField('Назва сайту', max_length=100, default='Затишний Двір')
    tagline = models.CharField('Слоган', max_length=200, blank=True)
    logo = models.ImageField('Логотип', upload_to='core/', blank=True)
    logo_white = models.ImageField('Логотип білий', upload_to='core/', blank=True)
    phone = models.CharField('Телефон', max_length=30, blank=True)
    phone_secondary = models.CharField('Телефон 2', max_length=30, blank=True)
    email = models.EmailField('Email', blank=True)
    address = models.CharField('Адреса', max_length=255, blank=True)
    map_embed = models.TextField('Embed код Google Maps', blank=True)
    hero_video = models.FileField('Відео для Hero', upload_to='core/video/', blank=True)
    hero_video_poster = models.ImageField('Постер для відео', upload_to='core/', blank=True)
    hero_eyebrow = models.CharField(
        'Підпис над заголовком Hero',
        max_length=100,
        default='SPA Resort • Буковель',
        help_text='Маленький текст над головним заголовком на першому екрані',
    )
    instagram_url = models.URLField('Instagram URL', blank=True)
    facebook_url = models.URLField('Facebook URL', blank=True)
    telegram_url = models.URLField('Telegram URL', blank=True)
    viber_url = models.URLField('Viber URL', blank=True)
    about_text = models.TextField('Текст "Про нас"', blank=True)
    about_image = models.ImageField('Фото "Про нас"', upload_to='core/', blank=True)
    check_in_time = models.CharField('Час заїзду', max_length=10, default='15:00')
    check_out_time = models.CharField('Час виїзду', max_length=10, default='11:00')

    class Meta:
        verbose_name = 'Налаштування сайту'
        verbose_name_plural = 'Налаштування сайту'

    def __str__(self):
        return self.site_name


class HeroSlide(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    subtitle = models.TextField('Підзаголовок', blank=True)
    image = models.ImageField('Зображення', upload_to='hero/', blank=True)
    cta_text = models.CharField('Текст кнопки', max_length=80, blank=True)
    cta_url = models.CharField('URL кнопки', max_length=200, blank=True, default='#booking')
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Активний', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Слайд Hero'
        verbose_name_plural = 'Слайди Hero'

    def __str__(self):
        return self.title


class StatItem(models.Model):
    value = models.CharField(
        'Значення',
        max_length=20,
        help_text='Наприклад: 22, 5★, 20×8, 2 хв',
    )
    label = models.CharField(
        'Підпис',
        max_length=100,
        help_text='Наприклад: Номерів та апартаментів',
    )
    order = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Відображати', default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Статистика на головній'
        verbose_name_plural = 'Статистика на головній'

    def __str__(self):
        return f'{self.value} — {self.label}'
