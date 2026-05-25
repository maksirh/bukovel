from modeltranslation.translator import register, TranslationOptions

from .models import SiteSettings, HeroSlide, StatItem


@register(SiteSettings)
class SiteSettingsTranslationOptions(TranslationOptions):
    fields = ('site_name', 'tagline', 'about_text', 'hero_eyebrow')


@register(HeroSlide)
class HeroSlideTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'cta_text')


@register(StatItem)
class StatItemTranslationOptions(TranslationOptions):
    fields = ('label',)
