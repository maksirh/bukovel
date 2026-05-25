from modeltranslation.translator import register, TranslationOptions

from .models import SpecialOffer


@register(SpecialOffer)
class SpecialOfferTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'description')
