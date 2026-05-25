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
from django.core.management.base import BaseCommand

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

        self.stdout.write(self.style.MIGRATE_HEADING("\n📦  seed_db — старт\n"))

        self._seed_site_settings()
        self._seed_hero_slides()
        self._seed_stat_items()
        self._seed_rooms()
        self._seed_spa()
        self._seed_restaurant()
        self._seed_services()
        self._seed_offers()

        self.stdout.write(self.style.SUCCESS("\n✅  seed_db — завершено\n"))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _copy_image(self, src_rel: str, dest_subdir: str) -> str:
        """
        Копіює файл з hotel_images/<src_rel> до media/<dest_subdir>/<unique_name>.
        Унікальне ім'я = src_rel із заміною '/' на '_', щоб уникнути
        колізій між main_img.png з різних підпапок.
        Якщо файл вже існує — пропускає копіювання.
        Якщо src_rel порожній — повертає порожній рядок без попередження.
        """
        if not src_rel:
            return ""

        src = IMAGES_SRC_ROOT / src_rel
        if not src.exists():
            self.stdout.write(
                self.style.WARNING(f"   ⚠  Зображення не знайдено: hotel_images/{src_rel}")
            )
            return ""

        dest_dir = MEDIA_ROOT / dest_subdir
        dest_dir.mkdir(parents=True, exist_ok=True)

        unique_name = src_rel.replace("/", "_")
        dest = dest_dir / unique_name
        if not dest.exists():
            shutil.copy2(src, dest)

        return f"{dest_subdir}/{unique_name}"

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
        about_img = self._copy_image(d["about_image_src"], "core")

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
        if about_img:
            obj.about_image = about_img
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
            img = self._copy_image(data["image_src"], "hero")
            obj, created = HeroSlide.objects.update_or_create(
                order=data["order"],
                defaults={
                    "title": data["title"],
                    "subtitle": data["subtitle"],
                    "cta_text": data["cta_text"],
                    "cta_url": data["cta_url"],
                    "is_active": data["is_active"],
                    "image": img,
                },
            )
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
            cover = self._copy_image(data["cover_image_src"], "rooms")

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
                    "cover_image": cover,
                },
            )
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
            img_path = self._copy_image(src, "rooms/gallery")
            if not img_path:
                continue
            RoomImage.objects.update_or_create(
                room_type=room,
                order=idx,
                defaults={"image": img_path, "alt": room.title},
            )

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
        cover = self._copy_image(d["cover_image_src"], "spa")
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
        if cover:
            schedule.cover_image = cover
        schedule.save()
        schedule.highlight_1_label_en = d["highlight_1_label_en"]  # type: ignore[attr-defined]
        schedule.highlight_2_label_en = d["highlight_2_label_en"]  # type: ignore[attr-defined]
        schedule.highlight_3_label_en = d["highlight_3_label_en"]  # type: ignore[attr-defined]
        schedule.save()
        self._ok("SpaSchedule", False)

        for data in SPA_ZONES_DATA:
            img = self._copy_image(data["image_src"], "spa")
            obj, created = SpaZone.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "title": data["title"],
                    "description": data["description"],
                    "order": data["order"],
                    "image": img,
                },
            )
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
            img = self._copy_image(data["image_src"], "spa/gallery")
            if not img:
                continue
            obj, created = SpaGallery.objects.update_or_create(
                order=data["order"],
                defaults={
                    "image": img,
                    "caption": data["caption"],
                },
            )
            obj.caption_en = data["caption_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(data["caption"], created)

    def _seed_restaurant(self) -> None:
        self.stdout.write("🍽  RestaurantInfo + MenuSection + MenuItem + RestaurantPhoto...")

        d = RESTAURANT_INFO_DATA
        cover = self._copy_image(d["cover_image_src"], "restaurant")
        info = RestaurantInfo.load()
        info.title = d["title"]
        info.description = d["description"]
        info.opening_hours = d["opening_hours"]
        info.breakfast_hours = d["breakfast_hours"]
        if cover:
            info.cover_image = cover
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
                img = self._copy_image(item_data.get("image_src", ""), "restaurant/menu")
                defaults = {
                    "title": item_data["title"],
                    "description": item_data["description"],
                    "price": item_data["price"],
                    "is_active": True,
                }
                if img:
                    defaults["image"] = img

                item, item_created = MenuItem.objects.update_or_create(
                    section=section,
                    order=item_data["order"],
                    defaults=defaults,
                )
                item.title_en = item_data["title_en"]  # type: ignore[attr-defined]
                item.description_en = item_data["description_en"]  # type: ignore[attr-defined]
                item.save()

        self._seed_restaurant_photos()

    def _seed_restaurant_photos(self) -> None:
        for data in RESTAURANT_PHOTOS_DATA:
            img = self._copy_image(data["image_src"], "restaurant/gallery")
            if not img:
                continue
            obj, created = RestaurantPhoto.objects.update_or_create(
                order=data["order"],
                defaults={
                    "image": img,
                    "alt": data["alt"],
                },
            )
            obj.alt_en = data["alt_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(data["alt"], created)

    def _seed_services(self) -> None:
        self.stdout.write("⚙️  Service...")
        for data in SERVICES_DATA:
            img = self._copy_image(data.get("image_src", ""), "services")
            defaults = {
                "title": data["title"],
                "short_description": data["short_description"],
                "description": data["description"],
                "icon": data["icon"],
                "order": data["order"],
                "is_active": data["is_active"],
            }
            if img:
                defaults["image"] = img

            obj, created = Service.objects.update_or_create(
                slug=data["slug"],
                defaults=defaults,
            )
            obj.title_en = data["title_en"]  # type: ignore[attr-defined]
            obj.short_description_en = data["short_description_en"]  # type: ignore[attr-defined]
            obj.description_en = data["description_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(obj.title, created)

    def _seed_offers(self) -> None:
        self.stdout.write("🏷  SpecialOffer...")
        for data in OFFERS_DATA:
            img = self._copy_image(data["image_src"], "offers")
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
                    "image": img,
                },
            )
            obj.title_en = data["title_en"]  # type: ignore[attr-defined]
            obj.subtitle_en = data["subtitle_en"]  # type: ignore[attr-defined]
            obj.description_en = data["description_en"]  # type: ignore[attr-defined]
            obj.save()
            self._ok(obj.title, created)
