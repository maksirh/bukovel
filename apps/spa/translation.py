from modeltranslation.translator import register, TranslationOptions

from .models import SpaZone, SpaSchedule, SpaPackage, SpaGallery


@register(SpaZone)
class SpaZoneTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(SpaSchedule)
class SpaScheduleTranslationOptions(TranslationOptions):
    fields = (
        'description',
        'highlight_1_label',
        'highlight_2_label',
        'highlight_3_label',
        'stat_1_label',
        'stat_2_label',
        'stat_3_label',
    )


@register(SpaPackage)
class SpaPackageTranslationOptions(TranslationOptions):
    fields = ('title', 'features')


@register(SpaGallery)
class SpaGalleryTranslationOptions(TranslationOptions):
    fields = ('caption',)
