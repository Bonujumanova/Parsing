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
}


def preprocess_categories_map(lang: str) -> dict[str, str]:
    base_url: str = SITE_URL[lang]

    categories: dict[str, str] = {}
    for url, names in CATEGORIES_MAP.items():
        name = names.get(lang)
        categories[name] = base_url + url

    return categories


if __name__ == '__main__':
    user_lang = input(f"Choose lang ({', '.join(SITE_URL)}): ")
    if user_lang not in SITE_URL:
        raise ValueError("Unavailable language")

    pprint(preprocess_categories_map(user_lang))
