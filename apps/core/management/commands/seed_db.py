"""
Management command: seed_db
Заповнює БД реальними даними та копіює зображення з hotel_images/ до media/.

Використання:
    python manage.py seed_db            # ідемпотентне заповнення
    python manage.py seed_db --clear    # очищення + повне заповнення
"""
import shutil
from datetime import date
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from apps.core.cloudinary_sync import cloudinary_configured, needs_cloudinary_upload
from apps.core.models import HeroSlide, SiteSettings, StatItem
from apps.offers.models import SpecialOffer
from apps.restaurant.models import MenuItem, MenuSection, RestaurantInfo, RestaurantPhoto
from apps.rooms.models import RoomFeature, RoomImage, RoomType
from apps.services.models import Service
from apps.spa.models import SpaGallery, SpaPackage, SpaSchedule, SpaZone

from ._seed_data import (
    HERO_SLIDES_DATA,
    OFFERS_DATA,
    SERVICES_DATA,
    SITE_SETTINGS_DATA,
    STAT_ITEMS_DATA,
)
from ._seed_data_restaurant import (
    RESTAURANT_INFO_DATA,
    RESTAURANT_MENU_DATA,
    RESTAURANT_PHOTOS_DATA,
)
from ._seed_data_rooms import ROOMS_DATA
from ._seed_data_spa import (
    SPA_GALLERY_DATA,
    SPA_PACKAGES_DATA,
    SPA_SCHEDULE_DATA,
    SPA_ZONES_DATA,
)

IMAGES_SRC_ROOT = Path(settings.BASE_DIR) / "hotel_images"
MEDIA_ROOT = Path(settings.MEDIA_ROOT)


class Command(BaseCommand):
    help = "Заповнює БД реальними даними та копіює зображення з hotel_images/"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Очистити існуючі дані перед заповненням (крім BookingRequest)",
        )

    # ------------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------------

    def handle(self, *args, **options):
        if options["clear"]:
            self._clear_data()

        from django.core.files.storage import default_storage

        self.stdout.write(self.style.MIGRATE_HEADING("\n📦  seed_db — старт\n"))
        self.stdout.write(f"   Storage: {default_storage.__class__.__name__}")
        cloud_name = settings.CLOUDINARY_STORAGE.get('CLOUD_NAME', '')
        if cloud_name:
            self.stdout.write(f"   Cloudinary: {cloud_name}")
        elif not settings.DEBUG:
            self.stdout.write(self.style.WARNING(
                "   ⚠  CLOUDINARY_CLOUD_NAME не заданий — фото не завантажаться на Cloudinary"
            ))

        self._images_ok = 0
        self._images_fail = 0
        self._images_skip = 0
        self._smart_sync = False
        self._force_images = False

        self._seed_site_settings()
        self._seed_hero_slides()
        self._seed_stat_items()
        self._seed_rooms()
        self._seed_spa()
        self._seed_restaurant()
        self._seed_services()
        self._seed_offers()

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅  seed_db — завершено "
                f"(фото: {self._images_ok} ok, {self._images_skip} пропущено, {self._images_fail} помилок)\n"
            )
        )

    def sync_all_images(self, *, smart: bool = True, force: bool = False) -> None:
        """Лише завантаження фото з hotel_images/ у наявні записи БД."""
        from django.core.files.storage import default_storage

        self._images_ok = 0
        self._images_fail = 0
        self._images_skip = 0
        self._smart_sync = smart
        self._force_images = force

        self.stdout.write(self.style.MIGRATE_HEADING("\n🖼  sync_all_images — старт\n"))
        self.stdout.write(f"   Storage: {default_storage.__class__.__name__}")
        if cloudinary_configured():
            self.stdout.write(f"   Cloudinary: {settings.CLOUDINARY_STORAGE['CLOUD_NAME']}")
        elif not settings.DEBUG:
            self.stdout.write(self.style.ERROR(
                "   ✖  CLOUDINARY_* env vars не задані — upload неможливий"
            ))
            return

        hotel_count = sum(1 for _ in IMAGES_SRC_ROOT.rglob('*') if _.is_file())
        self.stdout.write(f"   Файлів у hotel_images/: {hotel_count}")

        self._sync_site_settings_images()
        self._sync_hero_images()
        self._sync_rooms_images()
        self._sync_spa_images()
        self._sync_restaurant_images()
        self._sync_services_images()
        self._sync_offers_images()

        self.stdout.write(
            self.style.SUCCESS(
                f"\n✅  sync_all_images — завершено "
                f"(завантажено: {self._images_ok}, пропущено: {self._images_skip}, "
                f"помилок: {self._images_fail})\n"
            )
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _apply_image(self, instance, field_name: str, src_rel: str) -> None:
        """
        Завантажує файл з hotel_images/ у ImageField через storage backend.
        Працює локально (media/) і на prod (Cloudinary).
        """
        if not src_rel:
            return

        src = IMAGES_SRC_ROOT / src_rel
        if not src.exists():
            self.stdout.write(
                self.style.WARNING(f"   ⚠  Зображення не знайдено: hotel_images/{src_rel}")
            )
            return

        unique_name = src_rel.replace("/", "_")
        field = getattr(instance, field_name)

        if (
            self._smart_sync
            and not self._force_images
            and field.name
            and not needs_cloudinary_upload(
                field,
                verify_remote=getattr(self, '_verify_remote', False),
            )
        ):
            self._images_skip += 1
            return

        try:
            if field.name:
                field.delete(save=False)
            with src.open("rb") as fh:
                field.save(unique_name, File(fh), save=False)
            self._images_ok += 1
        except Exception as exc:
            self._images_fail += 1
            self.stdout.write(
                self.style.WARNING(
                    f"   ⚠  Не вдалось завантажити {src_rel}: {exc}"
                )
            )

    def _sync_site_settings_images(self) -> None:
        self.stdout.write("🏨  SiteSettings...")
        obj = SiteSettings.load()
        self._apply_image(obj, "about_image", SITE_SETTINGS_DATA["about_image_src"])
        obj.save()

    def _sync_hero_images(self) -> None:
        self.stdout.write("🖼  HeroSlide...")
        for data in HERO_SLIDES_DATA:
            obj = HeroSlide.objects.filter(order=data["order"]).first()
            if not obj:
                continue
            self._apply_image(obj, "image", data["image_src"])
            obj.save()

    def _sync_rooms_images(self) -> None:
        self.stdout.write("🛏  RoomType + RoomImage...")
        for data in ROOMS_DATA:
            room = RoomType.objects.filter(slug=data["slug"]).first()
            if not room:
                continue
            self._apply_image(room, "cover_image", data["cover_image_src"])
            room.save()
            for idx, src in enumerate(data["gallery_images"]):
                if not src:
                    continue
                img = RoomImage.objects.filter(room_type=room, order=idx).first()
                if not img:
                    continue
                self._apply_image(img, "image", src)
                img.save()

    def _sync_spa_images(self) -> None:
        self.stdout.write("💆  Spa...")
        schedule = SpaSchedule.load()
        self._apply_image(schedule, "cover_image", SPA_SCHEDULE_DATA["cover_image_src"])
        schedule.save()

        for data in SPA_ZONES_DATA:
            obj = SpaZone.objects.filter(slug=data["slug"]).first()
            if not obj:
                continue
            self._apply_image(obj, "image", data["image_src"])
            obj.save()

        for data in SPA_GALLERY_DATA:
            obj = SpaGallery.objects.filter(order=data["order"]).first()
            if not obj:
                continue
            self._apply_image(obj, "image", data["image_src"])
            obj.save()

    def _sync_restaurant_images(self) -> None:
        self.stdout.write("🍽  Restaurant...")
        info = RestaurantInfo.load()
        self._apply_image(info, "cover_image", RESTAURANT_INFO_DATA["cover_image_src"])
        info.save()

        for block in RESTAURANT_MENU_DATA:
            section = MenuSection.objects.filter(order=block["section"]["order"]).first()
            if not section:
                continue
            for item_data in block["items"]:
                item = MenuItem.objects.filter(
                    section=section, order=item_data["order"]
                ).first()
                if not item:
                    continue
                self._apply_image(item, "image", item_data.get("image_src", ""))
                item.save()

        for data in RESTAURANT_PHOTOS_DATA:
            obj = RestaurantPhoto.objects.filter(order=data["order"]).first()
            if not obj:
                continue
            self._apply_image(obj, "image", data["image_src"])
            obj.save()

    def _sync_services_images(self) -> None:
        self.stdout.write("⚙️  Service...")
        for data in SERVICES_DATA:
            obj = Service.objects.filter(slug=data["slug"]).first()
            if not obj:
                continue
            self._apply_image(obj, "image", data.get("image_src", ""))
            obj.save()

    def _sync_offers_images(self) -> None:
        self.stdout.write("🏷  SpecialOffer...")
        for data in OFFERS_DATA:
            obj = SpecialOffer.objects.filter(slug=data["slug"]).first()
            if not obj:
                continue
            self._apply_image(obj, "image", data["image_src"])
            obj.save()

    def _ok(self, label: str, created: bool) -> None:
        action = "створено" if created else "оновлено"
        self.stdout.write(f"   ✔  {label} [{action}]")

    def _clear_data(self) -> None:
        self.stdout.write(self.style.WARNING("🗑  Очищення даних..."))
        RoomImage.objects.all().delete()
        RoomFeature.objects.all().delete()
        RoomType.objects.all().delete()
        HeroSlide.objects.all().delete()
        StatItem.objects.all().delete()
        SpaZone.objects.all().delete()
        SpaPackage.objects.all().delete()
        SpaGallery.objects.all().delete()
        SpaSchedule.objects.filter(pk=1).delete()
        MenuSection.objects.all().delete()
        MenuItem.objects.all().delete()
        RestaurantPhoto.objects.all().delete()
        Service.objects.all().delete()
        SpecialOffer.objects.all().delete()

        for subdir in ("core", "hero", "rooms", "spa", "restaurant", "services", "offers"):
            target = MEDIA_ROOT / subdir
            if target.exists():
                shutil.rmtree(target)
                self.stdout.write(self.style.WARNING(f"   ✔  media/{subdir}/ очищено"))

        self.stdout.write(self.style.WARNING("   ✔  Дані очищено\n"))

    # ------------------------------------------------------------------
    # Seeding methods
    # ------------------------------------------------------------------

    def _seed_site_settings(self) -> None:
        self.stdout.write("🏨  SiteSettings...")
        d = SITE_SETTINGS_DATA

        obj = SiteSettings.load()
        obj.site_name = d["site_name"]
        obj.tagline = d["tagline"]
        obj.phone = d["phone"]
        obj.phone_secondary = d["phone_secondary"]
        obj.email = d["email"]
        obj.address = d["address"]
        obj.hero_eyebrow = d["hero_eyebrow"]
        obj.check_in_time = d["check_in_time"]
        obj.check_out_time = d["check_out_time"]
        obj.instagram_url = d["instagram_url"]
        obj.facebook_url = d["facebook_url"]
        obj.telegram_url = d["telegram_url"]
        obj.viber_url = d["viber_url"]
        obj.about_text = d["about_text"]
        self._apply_image(obj, "about_image", d["about_image_src"])
        obj.save()

        obj.site_name_en = d["site_name_en"]  # type: ignore[attr-defined]
        obj.tagline_en = d["tagline_en"]  # type: ignore[attr-defined]
        obj.hero_eyebrow_en = d["hero_eyebrow_en"]  # type: ignore[attr-defined]
        obj.about_text_en = d["about_text_en"]  # type: ignore[attr-defined]
        obj.save()

        self._ok("SiteSettings", False)

    def _seed_hero_slides(self) -> None:
        self.stdout.write("🖼  HeroSlide...")
        for data in HERO_SLIDES_DATA:
            obj, created = HeroSlide.objects.update_or_create(
                order=data["order"],
                defaults={
                    "title": data["title"],
                    "subtitle": data["subtitle"],
                    "cta_text": data["cta_text"],
                    "cta_url": data["cta_url"],
                    "is_active": data["is_active"],
                },
            )
            self._apply_image(obj, "image", data["image_src"])
            obj.save()
            obj.title_en = data["title_en"]  # type: ignore[attr-defined]
            obj.subtitle_en = data["subtitle_en"]  # type: ignore[attr-defined]
            obj.cta_text_en = data["cta_text_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(obj.title, created)

    def _seed_stat_items(self) -> None:
        self.stdout.write("📊  StatItem...")
        for data in STAT_ITEMS_DATA:
            obj, created = StatItem.objects.update_or_create(
                order=data["order"],
                defaults={
                    "value": data["value"],
                    "label": data["label"],
                    "is_active": True,
                },
            )
            obj.label_en = data["label_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(f'{data["value"]} — {data["label"]}', created)

    def _seed_rooms(self) -> None:
        self.stdout.write("🛏  RoomType + RoomImage + RoomFeature...")
        for data in ROOMS_DATA:
            room, created = RoomType.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "area_m2": data["area_m2"],
                    "max_guests": data["max_guests"],
                    "beds": data["beds"],
                    "rooms_count": data["rooms_count"],
                    "short_description": data["short_description"],
                    "description": data["description"],
                    "base_price": data["base_price"],
                    "order": data["order"],
                    "is_active": data["is_active"],
                },
            )
            self._apply_image(room, "cover_image", data["cover_image_src"])
            room.save()
            room.title_en = data["title_en"]  # type: ignore[attr-defined]
            room.short_description_en = data["short_description_en"]  # type: ignore[attr-defined]
            room.description_en = data["description_en"]  # type: ignore[attr-defined]
            room.beds_en = data["beds_en"]  # type: ignore[attr-defined]
            room.save()

            self._ok(room.title, created)

            self._seed_room_gallery(room, data["gallery_images"])
            self._seed_room_features(room, data["features"])

    def _seed_room_gallery(self, room: RoomType, images: list) -> None:
        for idx, src in enumerate(images):
            if not src:
                continue
            obj, _created = RoomImage.objects.update_or_create(
                room_type=room,
                order=idx,
                defaults={"alt": room.title},
            )
            self._apply_image(obj, "image", src)
            obj.save()

    def _seed_room_features(self, room: RoomType, features: list) -> None:
        for idx, feat in enumerate(features):
            obj, created = RoomFeature.objects.update_or_create(
                room_type=room,
                title=feat["title"],
                defaults={"icon": feat["icon"], "order": idx},
            )
            obj.title_en = feat["title_en"]  # type: ignore[attr-defined]
            obj.save()

    def _seed_spa(self) -> None:
        self.stdout.write("💆  SpaSchedule + SpaZone + SpaPackage + SpaGallery...")

        d = SPA_SCHEDULE_DATA
        schedule = SpaSchedule.load()
        schedule.working_hours = d["working_hours"]
        schedule.sauna_hours = d["sauna_hours"]
        schedule.description = d["description"]
        schedule.highlight_1_icon = d["highlight_1_icon"]
        schedule.highlight_1_label = d["highlight_1_label"]
        schedule.highlight_2_icon = d["highlight_2_icon"]
        schedule.highlight_2_label = d["highlight_2_label"]
        schedule.highlight_3_icon = d["highlight_3_icon"]
        schedule.highlight_3_label = d["highlight_3_label"]
        self._apply_image(schedule, "cover_image", d["cover_image_src"])
        schedule.save()
        schedule.highlight_1_label_en = d["highlight_1_label_en"]  # type: ignore[attr-defined]
        schedule.highlight_2_label_en = d["highlight_2_label_en"]  # type: ignore[attr-defined]
        schedule.highlight_3_label_en = d["highlight_3_label_en"]  # type: ignore[attr-defined]
        schedule.save()
        self._ok("SpaSchedule", False)

        for data in SPA_ZONES_DATA:
            obj, created = SpaZone.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "description": data["description"],
                    "order": data["order"],
                },
            )
            self._apply_image(obj, "image", data["image_src"])
            obj.save()
            obj.title_en = data["title_en"]  # type: ignore[attr-defined]
            obj.description_en = data["description_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(obj.title, created)

        self._seed_spa_packages()
        self._seed_spa_gallery()

    def _seed_spa_packages(self) -> None:
        for data in SPA_PACKAGES_DATA:
            obj, created = SpaPackage.objects.update_or_create(
                order=data["order"],
                defaults={
                    "title": data["title"],
                    "price": data["price"],
                    "duration": data["duration"],
                    "features": data["features"],
                    "is_popular": data["is_popular"],
                },
            )
            obj.title_en = data["title_en"]  # type: ignore[attr-defined]
            obj.features_en = data["features_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(obj.title, created)

    def _seed_spa_gallery(self) -> None:
        for data in SPA_GALLERY_DATA:
            obj, created = SpaGallery.objects.update_or_create(
                order=data["order"],
                defaults={"caption": data["caption"]},
            )
            self._apply_image(obj, "image", data["image_src"])
            obj.save()
            obj.caption_en = data["caption_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(data["caption"], created)

    def _seed_restaurant(self) -> None:
        self.stdout.write("🍽  RestaurantInfo + MenuSection + MenuItem + RestaurantPhoto...")

        d = RESTAURANT_INFO_DATA
        info = RestaurantInfo.load()
        info.title = d["title"]
        info.description = d["description"]
        info.opening_hours = d["opening_hours"]
        info.breakfast_hours = d["breakfast_hours"]
        self._apply_image(info, "cover_image", d["cover_image_src"])
        info.save()
        info.title_en = d["title_en"]  # type: ignore[attr-defined]
        info.description_en = d["description_en"]  # type: ignore[attr-defined]
        info.save()
        self._ok("RestaurantInfo", False)

        for block in RESTAURANT_MENU_DATA:
            sec_data = block["section"]
            section, created = MenuSection.objects.update_or_create(
                order=sec_data["order"],
                defaults={"title": sec_data["title"]},
            )
            section.title_en = sec_data["title_en"]  # type: ignore[attr-defined]
            section.save()
            self._ok(section.title, created)

            for item_data in block["items"]:
                defaults = {
                    "title": item_data["title"],
                    "description": item_data["description"],
                    "price": item_data["price"],
                    "is_active": True,
                }

                item, item_created = MenuItem.objects.update_or_create(
                    section=section,
                    order=item_data["order"],
                    defaults=defaults,
                )
                self._apply_image(item, "image", item_data.get("image_src", ""))
                item.save()
                item.title_en = item_data["title_en"]  # type: ignore[attr-defined]
                item.description_en = item_data["description_en"]  # type: ignore[attr-defined]
                item.save()

        self._seed_restaurant_photos()

    def _seed_restaurant_photos(self) -> None:
        for data in RESTAURANT_PHOTOS_DATA:
            obj, created = RestaurantPhoto.objects.update_or_create(
                order=data["order"],
                defaults={"alt": data["alt"]},
            )
            self._apply_image(obj, "image", data["image_src"])
            obj.save()
            obj.alt_en = data["alt_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(data["alt"], created)

    def _seed_services(self) -> None:
        self.stdout.write("⚙️  Service...")
        for data in SERVICES_DATA:
            defaults = {
                "title": data["title"],
                "short_description": data["short_description"],
                "description": data["description"],
                "icon": data["icon"],
                "order": data["order"],
                "is_active": data["is_active"],
            }

            obj, created = Service.objects.update_or_create(
                slug=data["slug"],
                defaults=defaults,
            )
            self._apply_image(obj, "image", data.get("image_src", ""))
            obj.save()
            obj.title_en = data["title_en"]  # type: ignore[attr-defined]
            obj.short_description_en = data["short_description_en"]  # type: ignore[attr-defined]
            obj.description_en = data["description_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(obj.title, created)

    def _seed_offers(self) -> None:
        self.stdout.write("🏷  SpecialOffer...")
        for data in OFFERS_DATA:
            obj, created = SpecialOffer.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "subtitle": data["subtitle"],
                    "description": data["description"],
                    "discount_percent": data["discount_percent"],
                    "valid_from": (
                        date.fromisoformat(data["valid_from"])
                        if data["valid_from"]
                        else None
                    ),
                    "valid_to": (
                        date.fromisoformat(data["valid_to"])
                        if data["valid_to"]
                        else None
                    ),
                    "is_active": data["is_active"],
                    "order": data["order"],
                },
            )
            self._apply_image(obj, "image", data["image_src"])
            obj.save()
            obj.title_en = data["title_en"]  # type: ignore[attr-defined]
            obj.subtitle_en = data["subtitle_en"]  # type: ignore[attr-defined]
            obj.description_en = data["description_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(obj.title, created)
