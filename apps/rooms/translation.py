from modeltranslation.translator import register, TranslationOptions

from .models import RoomType, RoomFeature


@register(RoomType)
class RoomTypeTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'description', 'beds')


@register(RoomFeature)
class RoomFeatureTranslationOptions(TranslationOptions):
    fields = ('title',)
