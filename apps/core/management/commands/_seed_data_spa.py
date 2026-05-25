"""
SPA-дані для seed_db management command.
Без Django-імпортів — лише структури даних.
"""

# ---------------------------------------------------------------------------
# Розклад та загальний опис SPA
# ---------------------------------------------------------------------------

SPA_SCHEDULE_DATA = {
    "working_hours": "08:00 – 22:00",
    "sauna_hours": "10:00 – 22:00",
    "description": (
        "Один з найбільших панорамних SPA у Буковелі площею понад 600 м². "
        "Відновіть тіло та розум в унікальній атмосфері карпатського релаксу: "
        "басейн 20×8 м з підігрівом, фінські сауни, хамам, дзеркальні джакузі, "
        "сінна кімната та масажні кабінети з преміум-процедурами."
    ),
    "cover_image_src": "spa_zones/pool/main_img.png",
    "highlight_1_icon": "🏊",
    "highlight_1_label": "Басейн 20×8 м",
    "highlight_1_label_en": "Pool 20×8 m",
    "highlight_2_icon": "🔥",
    "highlight_2_label": "6 зон оздоровлення",
    "highlight_2_label_en": "6 Wellness Zones",
    "highlight_3_icon": "🌿",
    "highlight_3_label": "600+ м² площа",
    "highlight_3_label_en": "600+ m² Area",
}

# ---------------------------------------------------------------------------
# Зони SPA
# ---------------------------------------------------------------------------

SPA_ZONES_DATA = [
    {
        "slug": "pool",
        "title": "Панорамний басейн 20×8 м",
        "title_en": "Panoramic Pool 20×8 m",
        "description": (
            "Один з найбільших панорамних басейнів у Буковелі з підігрівом води "
            "до 30°C. Розділений на зони: гідромасажні лежаки, інтенсивний масажний "
            "водоспад, зона джакузі та дитяча мілководна зона. Панорамні вікна "
            "від підлоги до стелі відкривають незабутній вид на карпатські вершини."
        ),
        "description_en": (
            "One of the largest panoramic pools in Bukovel, heated to 30°C. "
            "Divided into zones: hydromassage loungers, an intense massage waterfall, "
            "jacuzzi zone and children's shallow area. Floor-to-ceiling panoramic windows "
            "offer breathtaking views of the Carpathian peaks."
        ),
        "order": 1,
        "image_src": "spa_zones/pool/pool2.png",
    },
    {
        "slug": "saunas",
        "title": "Фінські сауни",
        "title_en": "Finnish Saunas",
        "description": (
            "Два різновиди фінських саун з натуральним деревом та ароматом "
            "карпатських трав. Перша — з м'якшим повітрям (70–75°C) для тривалого "
            "перебування. Друга — з інтенсивнішим паром (90–95°C) та соляними "
            "блоками для глибокого прогріву і детоксикації."
        ),
        "description_en": (
            "Two types of Finnish saunas with natural wood and Carpathian herb aromas. "
            "The first has milder air (70–75°C) for extended sessions. "
            "The second has more intense steam (90–95°C) with salt blocks "
            "for deep heating and detoxification."
        ),
        "order": 2,
        "image_src": "spa_zones/fin_sauna/main_img.png",
    },
    {
        "slug": "hammam",
        "title": "Хамам",
        "title_en": "Hammam",
        "description": (
            "Місце, де поєднуються традиції Сходу та сучасний комфорт. "
            "М'який вологий пар хамаму (45–50°C) допомагає зняти стрес, "
            "розслабити м'язи, відкрити пори та очистити шкіру. "
            "Мармуровий лежак з підігрівом, ароматичні ефірні олії, "
            "традиційний піллінг — атмосфера справжнього східного SPA."
        ),
        "description_en": (
            "A place where Eastern traditions meet modern comfort. "
            "The hammam's gentle moist steam (45–50°C) relieves stress, "
            "relaxes muscles, opens pores and cleanses the skin. "
            "Heated marble lounger, aromatic essential oils and traditional "
            "peeling — the atmosphere of a genuine Eastern SPA."
        ),
        "order": 3,
        "image_src": "spa_zones/khaman/main_img.png",
    },
    {
        "slug": "jacuzzi",
        "title": "Три джакузі",
        "title_en": "Three Jacuzzis",
        "description": (
            "Три унікальні дзеркальні джакузі з заспокійливою підсвіткою "
            "та декораціями у стилі карпатських гір. Температура води 37–38°C, "
            "масажні форсунки різної інтенсивності. Ідеальне місце для відновлення "
            "після лижного дня або просто для насолоди атмосферою."
        ),
        "description_en": (
            "Three unique mirror jacuzzis with soothing illumination "
            "and Carpathian mountain-style decor. Water temperature 37–38°C, "
            "massage jets of varying intensity. The perfect place to recover "
            "after a ski day or simply to enjoy the ambiance."
        ),
        "order": 4,
        "image_src": "spa_zones/jacuzzi/main_img.png",
    },
    {
        "slug": "hay-room",
        "title": "Сінна кімната",
        "title_en": "Hay Room",
        "description": (
            "Унікальний простір для повного розслаблення та ароматерапії. "
            "Кімната наповнена ароматом свіжого карпатського сіна та лікарських "
            "трав: ромашки, лаванди, меліси. Природні фітонциди трав заспокоюють "
            "нервову систему, покращують сон і дарують відчуття гармонії з природою."
        ),
        "description_en": (
            "A unique space for complete relaxation and aromatherapy. "
            "The room is filled with the scent of fresh Carpathian hay and medicinal "
            "herbs: chamomile, lavender, lemon balm. Natural phytoncides calm "
            "the nervous system, improve sleep and create a sense of harmony with nature."
        ),
        "order": 5,
        "image_src": "interior/rest_zone/027_OSACHUK-357.png",
    },
    {
        "slug": "massage",
        "title": "Масажні кабінети",
        "title_en": "Massage Rooms",
        "description": (
            "Шість масажних кабінетів з широким вибором процедур: класичний "
            "та релакс-масаж, глибоке тканинне скрабування, обгортання для "
            "омолодження та зволоження шкіри, LPG масаж тіла. "
            "Використовуємо виключно косметику люкс-сегменту від провідних "
            "European брендів. Рекомендуємо попереднє бронювання."
        ),
        "description_en": (
            "Six massage rooms offering a wide range of treatments: classic "
            "and relaxation massage, deep tissue scrub, anti-aging and moisturizing "
            "body wraps, LPG body massage. We use exclusively luxury cosmetics "
            "from leading European brands. Advance booking recommended."
        ),
        "order": 6,
        "image_src": "interior/rest_zone/028_OSACHUK-358.png",
    },
]

# ---------------------------------------------------------------------------
# Пакети SPA
# ---------------------------------------------------------------------------

SPA_PACKAGES_DATA = [
    {
        "title": "SPA Day",
        "title_en": "SPA Day",
        "price": 950,
        "duration": "3 години",
        "features": (
            "Панорамний басейн 20×8 м\n"
            "Фінська сауна (1 сеанс 30 хв)\n"
            "Джакузі\n"
            "Рушник та капці"
        ),
        "features_en": (
            "Panoramic pool 20×8 m\n"
            "Finnish sauna (1 session 30 min)\n"
            "Jacuzzi\n"
            "Towel and slippers"
        ),
        "is_popular": False,
        "order": 1,
    },
    {
        "title": "Relax Weekend",
        "title_en": "Relax Weekend",
        "price": 1450,
        "duration": "Необмежено",
        "features": (
            "Необмежений доступ до SPA\n"
            "Басейн, всі сауни, хамам\n"
            "Усі три джакузі\n"
            "Сінна кімната\n"
            "Рушник, халат, капці\n"
            "Фруктовий welcome drink"
        ),
        "features_en": (
            "Unlimited SPA access\n"
            "Pool, all saunas, hammam\n"
            "All three jacuzzis\n"
            "Hay room\n"
            "Towel, bathrobe, slippers\n"
            "Fruit welcome drink"
        ),
        "is_popular": True,
        "order": 2,
    },
    {
        "title": "Романтичний для двох",
        "title_en": "Romantic for Two",
        "price": 1800,
        "duration": "3 години • 2 особи",
        "features": (
            "VIP-доступ до всіх зон SPA\n"
            "Приватний джакузі (1 год)\n"
            "Масаж для двох (30 хв)\n"
            "Пляшка просекко\n"
            "Живі квіти та свічки\n"
            "Рушники, халати, капці"
        ),
        "features_en": (
            "VIP access to all SPA zones\n"
            "Private jacuzzi (1 hour)\n"
            "Couples massage (30 min)\n"
            "Bottle of prosecco\n"
            "Fresh flowers and candles\n"
            "Towels, bathrobes, slippers"
        ),
        "is_popular": False,
        "order": 3,
    },
]

# ---------------------------------------------------------------------------
# Галерея SPA
# ---------------------------------------------------------------------------

SPA_GALLERY_DATA = [
    {"image_src": "spa_zones/pool/pool3.png", "caption": "Панорамний басейн", "caption_en": "Panoramic Pool", "order": 1},
    {"image_src": "spa_zones/pool/pool4.png", "caption": "Панорамний басейн", "caption_en": "Panoramic Pool", "order": 2},
    {"image_src": "spa_zones/pool/pool5.png", "caption": "Зона релаксу", "caption_en": "Relaxation Zone", "order": 3},
    {"image_src": "spa_zones/pool/pool6.png", "caption": "Водний масаж", "caption_en": "Water Massage", "order": 4},
    {"image_src": "spa_zones/pool/pool7.png", "caption": "Панорамні вікна", "caption_en": "Panoramic Windows", "order": 5},
    {"image_src": "spa_zones/pool/pool8.png", "caption": "Дитяча зона", "caption_en": "Children's Zone", "order": 6},
    {"image_src": "spa_zones/fin_sauna/003_OSACHUK-331.png", "caption": "Фінська сауна", "caption_en": "Finnish Sauna", "order": 7},
    {"image_src": "spa_zones/fin_sauna/281_OSACHUK-254.png", "caption": "Парна зала", "caption_en": "Steam Room", "order": 8},
    {"image_src": "spa_zones/jacuzzi/025_OSACHUK-356.png", "caption": "Дзеркальне джакузі", "caption_en": "Mirror Jacuzzi", "order": 9},
    {"image_src": "spa_zones/jacuzzi/026_OSACHUK-355.png", "caption": "Джакузі з підсвіткою", "caption_en": "Illuminated Jacuzzi", "order": 10},
    {"image_src": "spa_zones/khaman/004_OSACHUK-334.png", "caption": "Хамам", "caption_en": "Hammam", "order": 11},
    {"image_src": "interior/rest_zone/011_OSACHUK-341.png", "caption": "Зона відпочинку", "caption_en": "Rest Zone", "order": 12},
]
