from django.db import models

from apps.core.models import SingletonModel


class SpaZone(models.Model):
    slug = models.SlugField('Slug', unique=True)
    title = models.CharField('Назва', max_length=150)
    description = models.TextField('Опис')
    image = models.ImageField('Зображення', upload_to='spa/', blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Зона SPA'
        verbose_name_plural = 'Зони SPA'

    def __str__(self):
        return self.title


class SpaSchedule(SingletonModel):
    working_hours = models.CharField('Години роботи SPA', max_length=50, default='08:00 – 22:00')
    sauna_hours = models.CharField('Години роботи парних', max_length=50, default='10:00 – 22:00')
    description = models.TextField('Загальний опис SPA', blank=True)
    cover_image = models.ImageField('Обкладинка SPA', upload_to='spa/', blank=True)

    highlight_1_icon = models.CharField('Іконка 1 (emoji або SVG id)', max_length=30, blank=True)
    highlight_1_label = models.CharField('Підпис 1', max_length=80, blank=True)
    highlight_2_icon = models.CharField('Іконка 2 (emoji або SVG id)', max_length=30, blank=True)
    highlight_2_label = models.CharField('Підпис 2', max_length=80, blank=True)
    highlight_3_icon = models.CharField('Іконка 3 (emoji або SVG id)', max_length=30, blank=True)
    highlight_3_label = models.CharField('Підпис 3', max_length=80, blank=True)

    stat_1_value = models.CharField('Стат. 1 — значення', max_length=20, default='600+')
    stat_1_label = models.CharField('Стат. 1 — підпис', max_length=80, default='м² площа SPA')
    stat_2_value = models.CharField('Стат. 2 — значення', max_length=20, default='20×8')
    stat_2_label = models.CharField('Стат. 2 — підпис', max_length=80, default='м панорамний басейн')
    stat_3_value = models.CharField('Стат. 3 — значення', max_length=20, default='6')
    stat_3_label = models.CharField('Стат. 3 — підпис', max_length=80, default='wellness-зон')

    class Meta:
        verbose_name = 'Розклад та опис SPA'
        verbose_name_plural = 'Розклад та опис SPA'

    def __str__(self):
        return 'SPA Розклад'


class SpaPackage(models.Model):
    title = models.CharField('Назва пакету', max_length=120)
    price = models.PositiveIntegerField('Ціна (грн)')
    duration = models.CharField('Тривалість', max_length=60)
    features = models.TextField('Склад пакету', help_text='По одному пункту на рядок')
    is_popular = models.BooleanField('Найпопулярніший', default=False)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Пакет SPA'
        verbose_name_plural = 'Пакети SPA'

    def __str__(self):
        return self.title

    def features_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class SpaGallery(models.Model):
    image = models.ImageField('Фото', upload_to='spa/gallery/')
    caption = models.CharField('Підпис', max_length=120, blank=True)
    order = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Фото галереї SPA'
        verbose_name_plural = 'Галерея SPA'

    def __str__(self):
        return self.caption or f'Фото {self.pk}'
