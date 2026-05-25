"""
Дані про типи номерів для seed_db management command.
"""

ROOMS_DATA = [
    {
        "slug": "standard",
        "title": "Стандартний номер",
        "title_en": "Standard Room",
        "area_m2": 28,
        "max_guests": 2,
        "beds": "1 ліжко king-size 180×200",
        "beds_en": "1 king-size bed 180×200",
        "rooms_count": 1,
        "short_description": "Затишний номер з ліжком king-size, балконом та виглядом на гори або басейн",
        "short_description_en": "Cozy room with a king-size bed, balcony and mountain or pool view",
        "description": (
            "Стандартний двомісний номер площею 28 м² з ліжком King-size 180×200, "
            "приватним балконом та сучасною ванною кімнатою з душовою кабіною. "
            "Кожен номер обладнаний системою клімат-контролю, смарт-телевізором, "
            "сейфом, феном та преміум-косметикою. Звукоізольовані вікна гарантують "
            "тишу та спокій навіть у пік сезону."
        ),
        "description_en": (
            "A standard double room of 28 m² with a King-size bed 180×200, "
            "private balcony and modern bathroom with shower. "
            "Each room is equipped with climate control, smart TV, safe, "
            "hairdryer and premium toiletries. Soundproof windows ensure "
            "peace and quiet even at peak season."
        ),
        "base_price": 2700,
        "order": 1,
        "is_active": True,
        "cover_image_src": "rooms/standart/main_img.png",
        "gallery_images": [
            "rooms/standart/048_OSACHUK-17.png",
            "rooms/standart/049_OSACHUK-18.png",
            "rooms/standart/050_OSACHUK-19.png",
            "rooms/standart/051_OSACHUK-20.png",
            "rooms/standart/052_OSACHUK-22.png",
            "rooms/standart/053_OSACHUK-21.png",
            "rooms/standart/054_OSACHUK-23.png",
            "rooms/standart/055_OSACHUK-24.png",
            "rooms/standart/061_OSACHUK-30.png",
            "rooms/standart/062_OSACHUK-31.png",
            "rooms/standart/063_OSACHUK-32.png",
            "rooms/standart/064_OSACHUK-33.png",
            "rooms/standart/065_OSACHUK-34.png",
            "rooms/standart/069_OSACHUK-38.png",
            "rooms/standart/070_OSACHUK-39.png",
            "rooms/standart/177_OSACHUK-150.png",
            "rooms/standart/178_OSACHUK-151.png",
            "rooms/standart/179_OSACHUK-152.png",
            "rooms/standart/180_OSACHUK-153.png",
            "rooms/standart/181_OSACHUK-154.png",
            "rooms/bathroom/042_OSACHUK-11.png",
            "rooms/bathroom/043_OSACHUK-12.png",
        ],
        "features": [
            {"icon": "🛏", "title": "Ліжко King-size 180×200", "title_en": "King-size bed 180×200"},
            {"icon": "🏔", "title": "Вид на гори або басейн", "title_en": "Mountain or pool view"},
            {"icon": "🚿", "title": "Душова кабіна", "title_en": "Shower cabin"},
            {"icon": "❄️", "title": "Клімат-контроль", "title_en": "Climate control"},
            {"icon": "📺", "title": "Смарт-телевізор", "title_en": "Smart TV"},
            {"icon": "🔒", "title": "Електронний сейф", "title_en": "Electronic safe"},
            {"icon": "🏊", "title": "Безкоштовний SPA", "title_en": "Free SPA access"},
        ],
    },
    {
        "slug": "apartments",
        "title": "Апартаменти",
        "title_en": "Apartments",
        "area_m2": 55,
        "max_guests": 5,
        "beds": "1 ліжко king-size + диван + дитяче ліжечко",
        "beds_en": "1 king-size bed + sofa + baby cot",
        "rooms_count": 2,
        "short_description": "Двокімнатні апартаменти з кухнею, терасою та панорамними вікнами для сімей та компаній",
        "short_description_en": "Two-bedroom apartments with kitchen, terrace and panoramic windows for families and groups",
        "description": (
            "Просторі двокімнатні апартаменти площею 55 м² з окремою спальнею, "
            "вітальнею та повністю обладнаною кухнею. Приватна тераса з виглядом "
            "на карпатський ліс та гірськолижні схили. Ванна кімната з великою "
            "ванною та окремою душовою кабіною. Ідеально для сімейного відпочинку "
            "або великої компанії. Надається дитяче ліжечко та стілець за запитом."
        ),
        "description_en": (
            "Spacious two-bedroom apartments of 55 m² with a separate bedroom, "
            "living room and fully equipped kitchen. Private terrace with views "
            "of the Carpathian forest and ski slopes. Bathroom with large bathtub "
            "and separate shower. Perfect for family vacations or groups. "
            "Baby cot and high chair available on request."
        ),
        "base_price": 5400,
        "order": 2,
        "is_active": True,
        "cover_image_src": "rooms/apartment/main_img.png",
        "gallery_images": [
            "rooms/apartment/076_OSACHUK-45.png",
            "rooms/apartment/077_OSACHUK-46.png",
            "rooms/apartment/078_OSACHUK-47.png",
            "rooms/apartment/079_OSACHUK-48.png",
            "rooms/apartment/080_OSACHUK-49.png",
            "rooms/apartment/081_OSACHUK-50.png",
            "rooms/apartment/082_OSACHUK-51.png",
            "rooms/apartment/083_OSACHUK-52.png",
            "rooms/apartment/085_OSACHUK-54.png",
            "rooms/apartment/086_OSACHUK-56.png",
            "rooms/apartment/087_OSACHUK-55.png",
            "rooms/apartment/088_OSACHUK-58.png",
            "rooms/apartment/090_OSACHUK-59.png",
            "rooms/apartment/096_OSACHUK-65.png",
            "rooms/apartment/097_OSACHUK-66.png",
            "rooms/launge/032_OSACHUK-1.png",
            "rooms/launge/033_OSACHUK-2.png",
            "rooms/launge/034_OSACHUK-3.png",
            "rooms/launge/035_OSACHUK-4.png",
            "rooms/launge/040_OSACHUK-9.png",
            "rooms/launge/041_OSACHUK-10.png",
            "rooms/kitchen/036_OSACHUK-5.png",
            "rooms/kitchen/037_OSACHUK-6.png",
            "rooms/kitchen/038_OSACHUK-7.png",
            "rooms/kitchen/039_OSACHUK-8.png",
            "rooms/bathroom/044_OSACHUK-13.png",
            "rooms/bathroom/045_OSACHUK-14.png",
            "rooms/bathroom/046_OSACHUK-15.png",
            "rooms/bathroom/071_OSACHUK-40.png",
            "rooms/bathroom/072_OSACHUK-41.png",
        ],
        "features": [
            {"icon": "🛏", "title": "Ліжко King-size + диван", "title_en": "King-size bed + sofa"},
            {"icon": "🍳", "title": "Повністю обладнана кухня", "title_en": "Fully equipped kitchen"},
            {"icon": "🛁", "title": "Ванна + душова кабіна", "title_en": "Bathtub + shower cabin"},
            {"icon": "🌅", "title": "Приватна тераса", "title_en": "Private terrace"},
            {"icon": "🏔", "title": "Панорамний вид на гори", "title_en": "Panoramic mountain view"},
            {"icon": "👶", "title": "Дитяче ліжечко за запитом", "title_en": "Baby cot on request"},
            {"icon": "❄️", "title": "Клімат-контроль", "title_en": "Climate control"},
            {"icon": "🏊", "title": "Безкоштовний SPA", "title_en": "Free SPA access"},
        ],
    },
    {
        "slug": "king-suite",
        "title": "Кінг Сюїт",
        "title_en": "King Suite",
        "area_m2": 45,
        "max_guests": 2,
        "beds": "1 ліжко king-size 200×200",
        "beds_en": "1 king-size bed 200×200",
        "rooms_count": 1,
        "short_description": "Розкішний сюїт із ліжком 200×200, гідромасажною ванною та панорамним виглядом на гори",
        "short_description_en": "Luxurious suite with 200×200 bed, hydromassage bathtub and panoramic mountain view",
        "description": (
            "Кінг Сюїт площею 45 м² — найпросторіший стандартний номер у готелі. "
            "Ліжко king-size 200×200 з ортопедичним матрацом, окрема зона відпочинку "
            "з диваном та журнальним столиком, ванна кімната з гідромасажною ванною "
            "та окремою дощовою душовою кабіною. "
            "Панорамні вікна з неповторним видом на карпатські вершини. "
            "Преміальна косметика, банний халат та капці включені."
        ),
        "description_en": (
            "The King Suite at 45 m² is the most spacious standard room in the hotel. "
            "A king-size 200×200 bed with an orthopedic mattress, a separate lounge area "
            "with sofa and coffee table, and a bathroom with a hydromassage bathtub "
            "and a separate rain shower cabin. "
            "Panoramic windows with breathtaking Carpathian mountain views. "
            "Premium toiletries, bathrobe and slippers included."
        ),
        "base_price": 3900,
        "order": 3,
        "is_active": True,
        "cover_image_src": "rooms/kingsuite/main_img.png",
        "gallery_images": [
            "rooms/kingsuite/119_OSACHUK-91.png",
            "rooms/kingsuite/120_OSACHUK-92.png",
            "rooms/kingsuite/121_OSACHUK-93.png",
            "rooms/kingsuite/122_OSACHUK-94.png",
            "rooms/kingsuite/123_OSACHUK-95.png",
            "rooms/kingsuite/124_OSACHUK-96.png",
            "rooms/kingsuite/125_OSACHUK-97.png",
            "rooms/kingsuite/130_OSACHUK-102.png",
            "rooms/kingsuite/138_OSACHUK-110.png",
            "rooms/kingsuite/139_OSACHUK-112.png",
            "rooms/kingsuite/141_OSACHUK-114.png",
            "rooms/kingsuite/142_OSACHUK-113.png",
            "rooms/kingsuite/143_OSACHUK-115.png",
            "rooms/kingsuite/145_OSACHUK-117.png",
            "rooms/kingsuite/156_OSACHUK-128.png",
            "rooms/kingsuite/157_OSACHUK-130.png",
            "rooms/kingsuite/158_OSACHUK-129.png",
            "rooms/kingsuite/159_OSACHUK-132.png",
            "rooms/kingsuite/160_OSACHUK-131.png",
            "rooms/kingsuite/161_OSACHUK-133.png",
            "rooms/kingsuite/162_OSACHUK-134.png",
            "rooms/bathroom/111_OSACHUK-83.png",
            "rooms/bathroom/112_OSACHUK-84.png",
            "rooms/bathroom/113_OSACHUK-85.png",
        ],
        "features": [
            {"icon": "🛏", "title": "Ліжко King-size 200×200", "title_en": "King-size bed 200×200"},
            {"icon": "🛁", "title": "Гідромасажна ванна", "title_en": "Hydromassage bathtub"},
            {"icon": "🚿", "title": "Дощова душова кабіна", "title_en": "Rain shower cabin"},
            {"icon": "🏔", "title": "Панорамний вид на гори", "title_en": "Panoramic mountain view"},
            {"icon": "❄️", "title": "Клімат-контроль", "title_en": "Climate control"},
            {"icon": "📺", "title": "Смарт-телевізор", "title_en": "Smart TV"},
            {"icon": "🔒", "title": "Електронний сейф", "title_en": "Electronic safe"},
            {"icon": "🏊", "title": "Безкоштовний SPA", "title_en": "Free SPA access"},
        ],
    },
    {
        "slug": "villa-delux",
        "title": "Вілла Делюкс",
        "title_en": "Villa Deluxe",
        "area_m2": 80,
        "max_guests": 6,
        "beds": "2 ліжка king-size + диван + 2 дитячі ліжечка",
        "beds_en": "2 king-size beds + sofa + 2 baby cots",
        "rooms_count": 3,
        "short_description": "Триповерхова вілла з приватним двором, камінним залом і панорамними терасами",
        "short_description_en": "Three-level villa with private courtyard, fireplace lounge and panoramic terraces",
        "description": (
            "Вілла Делюкс — найпрестижніший варіант розміщення у Затишному Дворі. "
            "Три рівні: спальня з ліжком king-size 200×200, вітальня з каміном, "
            "повністю обладнана кухня, дитяча кімната та два санвузли. "
            "Приватний внутрішній двір з місцем для барбекю, дві тераси з панорамним "
            "виглядом на Карпати та гірськолижні схили Буковелю. "
            "Ідеально для великих компаній та сімейного відпочинку преміум-рівня."
        ),
        "description_en": (
            "Villa Deluxe is the most prestigious accommodation at Cozy Yard. "
            "Three levels: a bedroom with a king-size 200×200 bed, a living room with fireplace, "
            "a fully equipped kitchen, a children's room and two bathrooms. "
            "A private courtyard with a barbecue area, two terraces with panoramic "
            "views of the Carpathians and Bukovel's ski slopes. "
            "Perfect for large groups and premium-level family getaways."
        ),
        "base_price": 9800,
        "order": 4,
        "is_active": True,
        "cover_image_src": "rooms/villa_delux/main_img.png",
        "gallery_images": [
            "rooms/villa_delux/169_OSACHUK-141.png",
            "rooms/villa_delux/171_OSACHUK-143.png",
            "rooms/villa_delux/172_OSACHUK-144.png",
            "rooms/villa_delux/173_OSACHUK-145.png",
            "rooms/bathroom/151_OSACHUK-123.png",
            "rooms/bathroom/152_OSACHUK-124.png",
            "rooms/bathroom/153_OSACHUK-125.png",
            "rooms/bathroom/154_OSACHUK-126.png",
            "rooms/bathroom/155_OSACHUK-127.png",
        ],
        "features": [
            {"icon": "🏡", "title": "Приватний двір з барбекю", "title_en": "Private courtyard with BBQ"},
            {"icon": "🔥", "title": "Камін у вітальні", "title_en": "Fireplace in living room"},
            {"icon": "🛏", "title": "2 ліжка King-size 200×200", "title_en": "2 King-size beds 200×200"},
            {"icon": "🍳", "title": "Повністю обладнана кухня", "title_en": "Fully equipped kitchen"},
            {"icon": "🌅", "title": "Дві панорамні тераси", "title_en": "Two panoramic terraces"},
            {"icon": "👶", "title": "Дитяча кімната", "title_en": "Children's room"},
            {"icon": "❄️", "title": "Клімат-контроль", "title_en": "Climate control"},
            {"icon": "🏊", "title": "Безкоштовний SPA", "title_en": "Free SPA access"},
        ],
    },
]
