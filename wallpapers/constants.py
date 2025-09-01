from pprint import pprint



SITE_URL: dict[str, str] = {
    "ru": "https://wallpaperscraft.ru/",
    "en": "https://wallpaperscraft.com/",
}


CATEGORIES_MAP: dict[str, dict[str, str]] = {
    'catalog/3d': {
        "ru": "3D",
        "en": "3D"
    },
    'catalog/abstract': {
        "ru": "Абстракция",
        "en": "Abstract"
    },
    'catalog/anime': {
        "ru": "Аниме",
        "en": "Anine"
    },
    'catalog/art': {
        "ru": "Арт",
        "en": "Art"
    },
    'catalog/vector': {
        "ru": "Вектор",
        "en": "Vector"
    },
    'catalog/city': {
        "ru": "Города",
        "en": "City"
    },
    'catalog/food': {
        "ru": "Еда",
        "en": "Food"
    },
    'catalog/animals': {
        "ru": "Животные",
        "en": "Food"
    },
    'catalog/space': {
        "ru": "space",
        "en": "Food"
    },
    'catalog/love': {
        "ru": "Любовь",
        "en": "Love"
    },
    'catalog/macro': {
        "ru": "Макро",
        "en": "Macro"
    },
    'catalog/cars': {
        "ru": "Машины",
        "en": "Cars"
    },
    'catalog/minimalism': {
        "ru": "Минимализм",
        "en": "Minimalism"
    },
    'catalog/motorcycles': {
        "ru": "Мотоциклы",
        "en": "Food"
    },
    'catalog/music': {
        "ru": "Музыка",
        "en": "Music"
    },
    'catalog/holidays': {
        "ru": "Праздники",
        "en": "Holidays"
    },
    'catalog/nature': {
        "ru": "Природа",
        "en": "Nature"
    },
    'catalog/other': {
        "ru": "Разное",
        "en": "Other"
    },
    'catalog/words': {
        "ru": "Слова",
        "en": "Words"
    },
    'catalog/sport': {
        "ru": "Спорт",
        "en": "Sport"
    },
    'catalog/textures': {
        "ru": "Текстуры",
        "en": "Textures"
    },
    'catalog/dark': {
        "ru": "Темные",
        "en": "Dark"
    },
    'catalog/technologies': {
        "ru": "Технологии",
        "en": "Technologies"
    },
    'catalog/fantasy': {
        "ru": "Фэнтези",
        "en": "Fantasy"
    },
    'catalog/flowers': {
        "ru": "Цветы",
        "en": "Flowers"
    },
    'catalog/black_and_white': {
        "ru": "Черно-белое",
        "en": "Black_and_white"
    },
    'catalog/black': {
        "ru": "Черный",
        "en": "Black"
    }


}


# keys = CATEGORIES_MAP["ru"].keys()
# values = list(value.replace('/catalog', "catalog") for value in CATEGORIES_MAP["ru"].values())
#
# pprint(
#     dict(zip(keys, values))
# )
