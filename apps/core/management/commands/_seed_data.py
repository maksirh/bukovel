"""
Чисті Python-константи для seed_db management command.
Без Django-імпортів — лише структури даних.
SPA-дані: _seed_data_spa.py
Ресторан:  _seed_data_restaurant.py
Номери:    _seed_data_rooms.py
"""

# ---------------------------------------------------------------------------
# Налаштування сайту
# ---------------------------------------------------------------------------

SITE_SETTINGS_DATA = {
    "site_name": "Затишний Двір",
    "site_name_en": "Cozy Yard",
    "tagline": "SPA Resort у серці Буковелю",
    "tagline_en": "SPA Resort in the Heart of Bukovel",
    "phone": "+38 (097) 000-00-00",
    "phone_secondary": "+38 (063) 000-00-00",
    "email": "info@zatyshnyi-dvir.com",
    "address": "с. Поляниця, Буковель, Івано-Франківська обл.",
    "hero_eyebrow": "SPA Resort • Буковель",
    "hero_eyebrow_en": "SPA Resort • Bukovel",
    "check_in_time": "15:00",
    "check_out_time": "11:00",
    "instagram_url": "https://instagram.com/zatyshnyi.dvir",
    "facebook_url": "",
    "telegram_url": "",
    "viber_url": "",
    "about_text": (
        "Готель Затишний Двір — це преміум-курорт у Буковелі, де поєднуються "
        "затишок карпатської садиби та рівень міжнародного готелю. "
        "Ми пропонуємо 22 номери та апартаменти з дизайнерським інтер'єром, "
        "панорамний SPA площею понад 600 м², ресторан м'яса та вина "
        "з видом на гірськолижні схили, а також безліч додаткових послуг "
        "для вашого ідеального відпочинку."
    ),
    "about_text_en": (
        "Cozy Yard Hotel is a premium resort in Bukovel that combines "
        "the warmth of a Carpathian estate with international hotel standards. "
        "We offer 22 designer rooms and apartments, a panoramic SPA of over 600 m², "
        "a meat and wine restaurant with mountain slope views, "
        "and a wide range of additional services for your perfect stay."
    ),
    "about_image_src": "interior/rest_zone/009_OSACHUK-339.png",
}

# ---------------------------------------------------------------------------
# Hero-слайди
# ---------------------------------------------------------------------------

HERO_SLIDES_DATA = [
    {
        "title": "Затишний Двір",
        "title_en": "Cozy Yard",
        "subtitle": "Преміум готель та SPA у серці Буковелю — для тих, хто цінує тишу, комфорт і красу Карпат",
        "subtitle_en": "Premium hotel and SPA in the heart of Bukovel — for those who value silence, comfort and the beauty of the Carpathians",
        "cta_text": "Забронювати",
        "cta_text_en": "Book Now",
        "cta_url": "#booking",
        "order": 0,
        "is_active": True,
        "image_src": "banners/main_page_banner.png",
    },
    {
        "title": "Панорамний SPA",
        "title_en": "Panoramic SPA",
        "subtitle": "Басейн 20×8 м, фінські сауни, хамам, джакузі та масажні кабінети — понад 600 м² релаксу",
        "subtitle_en": "20×8 m pool, Finnish saunas, hammam, jacuzzi and massage rooms — over 600 m² of relaxation",
        "cta_text": "Дізнатись більше",
        "cta_text_en": "Learn More",
        "cta_url": "/spa/",
        "order": 1,
        "is_active": True,
        "image_src": "spa_zones/pool/pool2.png",
    },
    {
        "title": "Ресторан м'яса та вина",
        "title_en": "Meat & Wine Restaurant",
        "subtitle": "Авторська кухня, карта благородних вин і панорамний вид на карпатські вершини",
        "subtitle_en": "Signature cuisine, a noble wine list and panoramic views of the Carpathian peaks",
        "cta_text": "Переглянути меню",
        "cta_text_en": "View Menu",
        "cta_url": "/restaurant/",
        "order": 2,
        "is_active": True,
        "image_src": "restaurant/hall/hall.png",
    },
    {
        "title": "Карпатська діжка",
        "title_en": "Carpathian Hot Tub",
        "subtitle": "Унікальне SPA під відкритим небом — дерев'яна діжка з підігрівом серед карпатської природи",
        "subtitle_en": "Unique open-air SPA — a heated wooden hot tub surrounded by Carpathian nature",
        "cta_text": "Забронювати",
        "cta_text_en": "Book Now",
        "cta_url": "#booking",
        "order": 3,
        "is_active": True,
        "image_src": "carpatian_hot_vat/hot_vat_main.png",
    },
]

# ---------------------------------------------------------------------------
# Статистика на головній
# ---------------------------------------------------------------------------

STAT_ITEMS_DATA = [
    {"value": "22", "label": "Номери та апартаменти", "label_en": "Rooms & Apartments", "order": 0},
    {"value": "20×8 м", "label": "Панорамний басейн", "label_en": "Panoramic Pool", "order": 1},
    {"value": "6", "label": "Зон SPA та оздоровлення", "label_en": "SPA & Wellness Zones", "order": 2},
    {"value": "2 хв", "label": "До підйомника 7R", "label_en": "To Ski Lift 7R", "order": 3},
]

# ---------------------------------------------------------------------------
# Послуги
# ---------------------------------------------------------------------------

SERVICES_DATA = [
    {
        "slug": "pets-friendly",
        "title": "Pets Friendly",
        "title_en": "Pets Friendly",
        "short_description": "Готель радо приймає гостей з пухнастими друзями до 7 кг",
        "short_description_en": "The hotel warmly welcomes guests with furry friends up to 7 kg",
        "description": (
            "Наш готель радо приймає гостей з домашніми тваринами вагою до 7 кг "
            "за невелику додаткову плату. Ми надаємо пеленку, рушник, лежанку, "
            "мисочки для води та їжі. Прохання повідомляти про тварину при бронюванні."
        ),
        "description_en": (
            "Our hotel warmly welcomes guests with pets up to 7 kg "
            "for a small additional fee. We provide a pad, towel, pet bed, "
            "and bowls for water and food. Please notify us about your pet when booking."
        ),
        "icon": "🐾",
        "image_src": "",
        "order": 1,
        "is_active": True,
    },
    {
        "slug": "kids-room",
        "title": "Дитяча ігрова кімната",
        "title_en": "Kids Play Room",
        "short_description": "Розваги для дітей усіх вікових груп із безпечним простором",
        "short_description_en": "Entertainment for children of all ages in a safe space",
        "description": (
            "У нашій дитячій кімнаті є все для веселого та безпечного дозвілля: "
            "інтерактивна освітня зона, гірка та м'який басейн з кульками, "
            "іграшки, настільні ігри та конструктори LEGO. "
            "Кімната обладнана системою відеоспостереження та безпечними "
            "покриттями на підлозі."
        ),
        "description_en": (
            "Our kids room has everything for fun and safe leisure: "
            "an interactive educational zone, slide and soft ball pool, "
            "toys, board games and LEGO sets. "
            "The room is equipped with CCTV and safe floor coverings."
        ),
        "icon": "🎠",
        "image_src": "children_room/main_img.png",
        "order": 2,
        "is_active": True,
    },
    {
        "slug": "carpathian-hot-tub",
        "title": "Карпатська діжка",
        "title_en": "Carpathian Hot Tub",
        "short_description": "Дерев'яна купіль із підігрівом на свіжому повітрі — унікальний досвід серед Карпат",
        "short_description_en": "Heated wooden outdoor hot tub — a unique experience amid the Carpathians",
        "description": (
            "Справжня карпатська дубова діжка встановлена просто неба: "
            "вода нагрівається до 37–40°C, у зимовий час навколо лежить сніг, "
            "а в повітрі — аромат хвої. "
            "Ідеально після лижного дня або як вечірній ритуал відновлення. "
            "Місткість: до 4 осіб. Бронювання за 2 години наперед. "
            "Аксесуари (рушники, халати) включені."
        ),
        "description_en": (
            "A genuine Carpathian oak hot tub installed in the open air: "
            "water heated to 37–40°C, surrounded by snow in winter "
            "and the scent of pine trees. "
            "Perfect after a ski day or as an evening recovery ritual. "
            "Capacity: up to 4 people. Booking 2 hours in advance required. "
            "Accessories (towels, robes) included."
        ),
        "icon": "🛁",
        "image_src": "carpatian_hot_vat/hot_vat_main.png",
        "order": 3,
        "is_active": True,
    },
    {
        "slug": "parking",
        "title": "Критий паркінг",
        "title_en": "Covered Parking",
        "short_description": "Захищений паркінг з цілодобовим відеоспостереженням",
        "short_description_en": "Secured parking with 24/7 CCTV surveillance",
        "description": (
            "Просторий і сучасний критий паркінг безпосередньо при готелі "
            "обладнаний найновішими системами безпеки та цілодобовим "
            "відеоспостереженням. Місця для звичайних автомобілів та SUV. "
            "Зарядка для електромобілів — за запитом."
        ),
        "description_en": (
            "A spacious modern covered parking lot directly at the hotel, "
            "equipped with the latest security systems and 24/7 CCTV. "
            "Spaces for standard cars and SUVs. "
            "EV charging available on request."
        ),
        "icon": "🅿️",
        "image_src": "",
        "order": 4,
        "is_active": True,
    },
    {
        "slug": "ski-room",
        "title": "Лижна кімната",
        "title_en": "Ski Room",
        "short_description": "Сховище та сушіння спорядження — підйомник 7R за 2 хвилини",
        "short_description_en": "Equipment storage and drying — ski lift 7R just 2 minutes away",
        "description": (
            "Спеціальна лижна кімната для зручного зберігання та сушіння "
            "гірськолижного спорядження з індивідуальними шафами і системою "
            "обігріву. До підйомника 7R від готелю — лише 2 хвилини пішки. "
            "Прокат лиж та сноубордів організовується за запитом."
        ),
        "description_en": (
            "A dedicated ski room for convenient storage and drying of ski equipment "
            "with individual lockers and a heating system. "
            "Only a 2-minute walk to ski lift 7R. "
            "Ski and snowboard rental available on request."
        ),
        "icon": "🎿",
        "image_src": "skis/main_img.png",
        "order": 5,
        "is_active": True,
    },
]

# ---------------------------------------------------------------------------
# Спецпропозиції
# ---------------------------------------------------------------------------

OFFERS_DATA = [
    {
        "slug": "summer-early-booking",
        "title": "Раннє бронювання — літо 2026",
        "title_en": "Early Booking — Summer 2026",
        "subtitle": "Плануйте відпочинок заздалегідь та заощаджуйте –10%",
        "subtitle_en": "Plan your vacation in advance and save 10%",
        "description": (
            "Ми відкриваємо раннє бронювання на літній сезон 2026 у Затишному Дворі "
            "зі знижкою –10% на всі типи номерів. "
            "Забронюйте зараз і насолоджуйтесь непередбачуваною красою Карпат улітку: "
            "трекінг, велопоходи, SPA під зірковим небом та ресторан з терасою. "
            "Пропозиція діє до 1 червня 2026."
        ),
        "description_en": (
            "We are opening early booking for the summer 2026 season at Cozy Yard "
            "with a 10% discount on all room types. "
            "Book now and enjoy the unpredictable beauty of the Carpathians in summer: "
            "trekking, cycling, SPA under the stars and a restaurant with a terrace. "
            "Offer valid until June 1, 2026."
        ),
        "discount_percent": 10,
        "valid_from": "2026-05-01",
        "valid_to": "2026-08-31",
        "is_active": True,
        "order": 1,
        "image_src": "exterior/257_OSACHUK-230.png",
    },
    {
        "slug": "weekend-spa",
        "title": "SPA-вихідні для двох",
        "title_en": "SPA Weekend for Two",
        "subtitle": "2 ночі + необмежений SPA + сніданки + вино при заселенні",
        "subtitle_en": "2 nights + unlimited SPA + breakfasts + wine on arrival",
        "description": (
            "Ексклюзивний романтичний SPA-пакет для пар: 2 ночі в номері на вибір, "
            "необмежений доступ до SPA-зони (басейн, сауни, хамам, джакузі) протягом "
            "усього перебування, сніданки щодня, пляшка преміум-вина та живі квіти "
            "при заселенні. Наш романтичний пакет — ідеальний подарунок для закоханих."
        ),
        "description_en": (
            "An exclusive romantic SPA package for couples: 2 nights in a room of your choice, "
            "unlimited SPA access (pool, saunas, hammam, jacuzzi) throughout your stay, "
            "daily breakfasts, a bottle of premium wine and fresh flowers on arrival. "
            "Our romantic package is the perfect gift for couples."
        ),
        "discount_percent": 0,
        "valid_from": None,
        "valid_to": None,
        "is_active": True,
        "order": 2,
        "image_src": "spa_zones/pool/pool3.png",
    },
    {
        "slug": "ski-season",
        "title": "Зимовий гірськолижний пакет",
        "title_en": "Winter Ski Package",
        "subtitle": "3 ночі + підйомник 7R + SPA + трансфер зі Львова",
        "subtitle_en": "3 nights + ski lift 7R + SPA + transfer from Lviv",
        "description": (
            "Повний зимовий пакет для любителів гір: 3 ночі в номері Стандарт або "
            "Апартаментах, ски-пас на підйомник 7R, щоденний необмежений SPA, "
            "сніданки та вечері в ресторані, трансфер зі Львова та назад. "
            "Лижна кімната з сушильними шафами включена."
        ),
        "description_en": (
            "A complete winter package for mountain lovers: 3 nights in a Standard Room "
            "or Apartments, ski pass for lift 7R, daily unlimited SPA, "
            "breakfasts and dinners at the restaurant, transfer from Lviv and back. "
            "Ski room with drying lockers included."
        ),
        "discount_percent": 15,
        "valid_from": "2026-12-01",
        "valid_to": "2027-03-15",
        "is_active": True,
        "order": 3,
        "image_src": "exterior/260_OSACHUK-233.png",
    },
]
