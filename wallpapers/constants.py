from pprint import pprint

SITE_URL: dict[str, str] = {
    "ru": "https://wallpaperscraft.ru/",
    "en": "https://wallpaperscraft.com/",
}

CATEGORIES_MAP: dict[str, dict[str, str]] = {
    "ru": {
        '3D': 'https://wallpaperscraft.ru/catalog/3d',
        'Абстракция': 'https://wallpaperscraft.ru/catalog/abstract',
        'Аниме': 'https://wallpaperscraft.ru/catalog/anime',
        'Арт': 'https://wallpaperscraft.ru/catalog/art',
        'Вектор': 'https://wallpaperscraft.ru/catalog/vector',
        'Города': 'https://wallpaperscraft.ru/catalog/city',
        'Еда': 'https://wallpaperscraft.ru/catalog/food',
        'Животные': 'https://wallpaperscraft.ru/catalog/animals',
        'Космос': 'https://wallpaperscraft.ru/catalog/space',
        'Любовь': 'https://wallpaperscraft.ru/catalog/love',
        'Макро': 'https://wallpaperscraft.ru/catalog/macro',
        'Машины': 'https://wallpaperscraft.ru/catalog/cars',
        'Минимализм': 'https://wallpaperscraft.ru/catalog/minimalism',
        'Мотоциклы': 'https://wallpaperscraft.ru/catalog/motorcycles',
        'Музыка': 'https://wallpaperscraft.ru/catalog/music',
        'Праздники': 'https://wallpaperscraft.ru/catalog/holidays',
        'Природа': 'https://wallpaperscraft.ru/catalog/nature',
        'Разное': 'https://wallpaperscraft.ru/catalog/other',
        'Слова': 'https://wallpaperscraft.ru/catalog/words',
        'Спорт': 'https://wallpaperscraft.ru/catalog/sport',
        'Текстуры': 'https://wallpaperscraft.ru/catalog/textures',
        'Темные': 'https://wallpaperscraft.ru/catalog/dark',
        'Технологии': 'https://wallpaperscraft.ru/catalog/hi-tech',
        'Фэнтези': 'https://wallpaperscraft.ru/catalog/fantasy',
        'Цветы': 'https://wallpaperscraft.ru/catalog/flowers',
        'Черно-белое': 'https://wallpaperscraft.ru/catalog/black_and_white',
        'Черный': 'https://wallpaperscraft.ru/catalog/black'
    },
    "en": {
        '3D': 'https://wallpaperscraft.com/catalog/3d',
        'Abstract': 'https://wallpaperscraft.com/catalog/abstract',
        'Anime': 'https://wallpaperscraft.com/catalog/anime',
        # ...

    }
}

# keys = CATEGORIES_MAP["ru"].keys()
# values = list(value.replace('/catalog', "catalog") for value in CATEGORIES_MAP["ru"].values())
#
# pprint(
#     dict(zip(keys, values))
# )
