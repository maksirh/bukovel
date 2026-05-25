"""
Дані ресторану для seed_db management command.
Без Django-імпортів — лише структури даних.
"""

# ---------------------------------------------------------------------------
# Загальна інформація про ресторан
# ---------------------------------------------------------------------------

RESTAURANT_INFO_DATA = {
    "title": "Ресторан м'яса та вина",
    "title_en": "Meat & Wine Restaurant",
    "description": (
        "Ми приділили увагу кожній деталі: ретельно пропрацьовані авторські страви, "
        "карта благородних вин понад 80 позицій, затишний інтер'єр у стилі "
        "карпатського шале, приємна жива музика у вихідні дні та м'яке "
        "свічкове освітлення. З панорамних вікон відкривається особливий вид "
        "на карпатський ліс та гірськолижні схили Буковелю."
    ),
    "description_en": (
        "We paid attention to every detail: carefully crafted signature dishes, "
        "a noble wine list of over 80 positions, a cozy Carpathian chalet-style interior, "
        "live music on weekends and soft candlelight. "
        "The panoramic windows offer a breathtaking view of the Carpathian forest "
        "and Bukovel's ski slopes."
    ),
    "opening_hours": "13:00 – 23:00",
    "breakfast_hours": "08:00 – 11:00",
    "cover_image_src": "restaurant/menu_brochure/main_img.png",
}

# ---------------------------------------------------------------------------
# Меню ресторану
# ---------------------------------------------------------------------------

RESTAURANT_MENU_DATA = [
    {
        "section": {"title": "Закуски та салати", "title_en": "Starters & Salads", "order": 1},
        "items": [
            {
                "title": "Карпатський лосось",
                "title_en": "Carpathian Salmon",
                "description": "Слабосолений лосось, крем-сир, каперси, житній хліб",
                "description_en": "Lightly salted salmon, cream cheese, capers, rye bread",
                "price": 320,
                "order": 1,
                "image_src": "restaurant/foods/nibbles5.png",
            },
            {
                "title": "Брускета з трюфелем",
                "title_en": "Truffle Bruschetta",
                "description": "Хрустка чіабата, трюфельна паста, пармезан, руккола",
                "description_en": "Crispy ciabatta, truffle paste, parmesan, arugula",
                "price": 240,
                "order": 2,
                "image_src": "restaurant/foods/nibbles2.png",
            },
            {
                "title": "Салат Цезар з куркою",
                "title_en": "Caesar Salad with Chicken",
                "description": "Смажена куряча грудка, крутони, пармезан, соус Цезар",
                "description_en": "Grilled chicken breast, croutons, parmesan, Caesar dressing",
                "price": 280,
                "order": 3,
                "image_src": "restaurant/foods/coleslaw.png",
            },
            {
                "title": "Крем-суп з грибами",
                "title_en": "Mushroom Cream Soup",
                "description": "Лісові гриби, вершки, трюфельна олія, зелень",
                "description_en": "Wild mushrooms, cream, truffle oil, herbs",
                "price": 210,
                "order": 4,
                "image_src": "restaurant/foods/garnish.png",
            },
        ],
    },
    {
        "section": {"title": "М'ясні страви", "title_en": "Meat Dishes", "order": 2},
        "items": [
            {
                "title": "Рібай Angus 300 г",
                "title_en": "Ribeye Angus 300 g",
                "description": "Стейк із яловичини Angus, вершкова картопля, соус Беарнез",
                "description_en": "Angus beef steak, creamy potatoes, Béarnaise sauce",
                "price": 890,
                "order": 1,
                "image_src": "restaurant/foods/meat_dishes.png",
            },
            {
                "title": "Томагавк Angus 800 г",
                "title_en": "Tomahawk Angus 800 g",
                "description": "Преміум-стейк на ребрі, гриль-овочі, соус Чімічуррі",
                "description_en": "Premium bone-in steak, grilled vegetables, Chimichurri sauce",
                "price": 1850,
                "order": 2,
                "image_src": "restaurant/foods/meat_platter.png",
            },
            {
                "title": "Баранячі реберця",
                "title_en": "Lamb Ribs",
                "description": "Мариновані реберця ягняти, розмарин, часниковий соус",
                "description_en": "Marinated lamb ribs, rosemary, garlic sauce",
                "price": 680,
                "order": 3,
                "image_src": "restaurant/foods/meat_dishes2.png",
            },
            {
                "title": "Качина грудка конфі",
                "title_en": "Duck Breast Confit",
                "description": "Качина грудка, апельсиновий соус, карамелізований буряк",
                "description_en": "Duck breast confit, orange sauce, caramelized beet",
                "price": 560,
                "order": 4,
                "image_src": "restaurant/foods/general_photo_dishes.png",
            },
            {
                "title": "Свиняча вирізка",
                "title_en": "Pork Tenderloin",
                "description": "Вирізка у медово-гірчичному маринаді, пюре, квашена капуста",
                "description_en": "Tenderloin in honey-mustard marinade, mashed potato, sauerkraut",
                "price": 420,
                "order": 5,
                "image_src": "restaurant/foods/general_photo_dishes2.png",
            },
        ],
    },
    {
        "section": {"title": "Сніданки", "title_en": "Breakfasts", "order": 3},
        "items": [
            {
                "title": "Сирники з ягодами",
                "title_en": "Cottage Cheese Pancakes with Berries",
                "description": "Домашні сирники, свіжі ягоди, сметана, варення",
                "description_en": "Homemade cottage cheese pancakes, fresh berries, sour cream, jam",
                "price": 180,
                "order": 1,
                "image_src": "restaurant/foods/syrnyky.png",
            },
            {
                "title": "Вишневі млинці",
                "title_en": "Cherry Pancakes",
                "description": "Тонкі млинці, вишнева начинка, збиті вершки, цукрова пудра",
                "description_en": "Thin pancakes, cherry filling, whipped cream, powdered sugar",
                "price": 165,
                "order": 2,
                "image_src": "restaurant/foods/cherry_pancakes.png",
            },
            {
                "title": "Яєчня з беконом",
                "title_en": "Eggs with Bacon",
                "description": "Три яйця, хрусткий бекон, тости, масло та джем",
                "description_en": "Three eggs, crispy bacon, toast, butter and jam",
                "price": 145,
                "order": 3,
                "image_src": "restaurant/foods/fried_egg.png",
            },
            {
                "title": "Круасан з вершковим сиром",
                "title_en": "Croissant with Cream Cheese",
                "description": "Свіжий круасан, вершковий сир, авокадо, зелень",
                "description_en": "Fresh croissant, cream cheese, avocado, herbs",
                "price": 125,
                "order": 4,
                "image_src": "restaurant/foods/croissant.png",
            },
        ],
    },
    {
        "section": {"title": "Десерти", "title_en": "Desserts", "order": 4},
        "items": [
            {
                "title": "Шоколадний фондан",
                "title_en": "Chocolate Fondant",
                "description": "Теплий шоколадний кекс з рідкою начинкою, ванільне морозиво",
                "description_en": "Warm chocolate cake with liquid filling, vanilla ice cream",
                "price": 195,
                "order": 1,
                "image_src": "restaurant/foods/baking1.png",
            },
            {
                "title": "Тірамісу",
                "title_en": "Tiramisu",
                "description": "Класичне тірамісу з маскарпоне та каво-лікерним просоченням",
                "description_en": "Classic tiramisu with mascarpone and coffee liqueur soaking",
                "price": 185,
                "order": 2,
                "image_src": "restaurant/foods/baking3.png",
            },
            {
                "title": "Карпатський яблучний штрудель",
                "title_en": "Carpathian Apple Strudel",
                "description": "Листкове тісто, карамелізовані яблука, кориця, збиті вершки",
                "description_en": "Puff pastry, caramelized apples, cinnamon, whipped cream",
                "price": 165,
                "order": 3,
                "image_src": "restaurant/foods/baking5.png",
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# Фотографії ресторану (для каруселі)
# ---------------------------------------------------------------------------

RESTAURANT_PHOTOS_DATA = [
    {"image_src": "restaurant/hall/hall.png", "alt": "Зал ресторану", "alt_en": "Restaurant Hall", "order": 1},
    {"image_src": "restaurant/hall/hall2.png", "alt": "Інтер'єр ресторану", "alt_en": "Restaurant Interior", "order": 2},
    {"image_src": "restaurant/hall/hall3.png", "alt": "Стола у залі", "alt_en": "Dining Tables", "order": 3},
    {"image_src": "restaurant/hall/hall4.png", "alt": "Атмосфера ресторану", "alt_en": "Restaurant Atmosphere", "order": 4},
    {"image_src": "restaurant/hall/hall5.png", "alt": "Панорамні вікна", "alt_en": "Panoramic Windows", "order": 5},
    {"image_src": "restaurant/hall/entry_hall.png", "alt": "Вхід до ресторану", "alt_en": "Restaurant Entrance", "order": 6},
    {"image_src": "restaurant/bar/main_bar.png", "alt": "Головний бар", "alt_en": "Main Bar", "order": 7},
    {"image_src": "restaurant/bar/bar.png", "alt": "Барна стійка", "alt_en": "Bar Counter", "order": 8},
    {"image_src": "restaurant/bar/bar2.png", "alt": "Карта вин", "alt_en": "Wine Selection", "order": 9},
    {"image_src": "restaurant/bar/bar3.png", "alt": "Колекція вин", "alt_en": "Wine Collection", "order": 10},
    {"image_src": "restaurant/menu_brochure/menu_brochure.png", "alt": "Меню ресторану", "alt_en": "Restaurant Menu", "order": 11},
    {"image_src": "restaurant/foods/general_photo_dishes3.png", "alt": "Авторські страви", "alt_en": "Signature Dishes", "order": 12},
]
