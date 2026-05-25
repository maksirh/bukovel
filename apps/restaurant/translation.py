from modeltranslation.translator import register, TranslationOptions

from .models import RestaurantInfo, MenuSection, MenuItem, RestaurantPhoto


@register(RestaurantInfo)
class RestaurantInfoTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(MenuSection)
class MenuSectionTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(MenuItem)
class MenuItemTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(RestaurantPhoto)
class RestaurantPhotoTranslationOptions(TranslationOptions):
    fields = ('alt',)
