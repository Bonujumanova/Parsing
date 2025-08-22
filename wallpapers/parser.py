import time

import requests
from bs4 import BeautifulSoup

from wallpapers.constants import CATEGORIES_MAP, SITE_URL


def show_categories(categories: dict[str, str]) -> None:
    # TODO: Реализовать вывод пронумерованных категорий
    pass


def show_images(data: dict[str, list]) -> None:
    # TODO: Реализовать вывод пронумерованных картинок:
    #  - Название
    #  - Ключевые слова
    #  - Абсолютная ссылка
    pass


def parse_images_on_page(curr_page: str) -> dict[str, list]:
    soup = BeautifulSoup(curr_page, features="html.parser")
    all_images = set(soup.find("ul", class_="wallpapers__list"))

    data: dict[str, list] = {}
    for i, li in enumerate(all_images, 1):
        item = li.find_next("a", class_="wallpapers__link")
        link = item.get("href")

        preview = item.find_next(
            "img",
            class_="wallpapers__image"
        ).attrs.get("alt", "Not previews").split(", ")
        data[link] = preview

    return data


def get_category_page(link: str, page_num: int) -> str:
    response = requests.get(f"{link}/page{page_num}/")

    if response.status_code == 200:
        return response.text

    if response.status_code == 404:
        raise ValueError("Page not found")

    raise ValueError("Something wrong")


def get_category(
        categories: dict[str, str], number: int
) -> tuple[str, str]:
    category_name = list(categories.keys())[number - 1]
    category_link = categories.get(category_name)

    return category_name, category_link


def main():
    choice_lang = input("Choice language (en, ru): ").lower()

    if choice_lang not in ("en", "ru"):
        raise ValueError("Unavailable language")

    categories = CATEGORIES_MAP.get(choice_lang)
    show_categories(categories)

    choice_category_number: int = int(input("Select category number: "))
    categories_length: int = len(categories)
    if not (1 <= choice_category_number <= categories_length):
        raise ValueError("Unavailable category")

    category_name, category_link = get_category(categories,
                                                choice_category_number)

    print(f"Selected category '{category_name}' - {category_link}")

    for page_num in range(1, 5):
        curr_page: str = get_category_page(category_link, page_num)

        images_on_page: dict[str, list] = parse_images_on_page(curr_page)
        print(images_on_page)
        time.sleep(10)

        # TODO: Доработать логику выбора картинки, скачать все
        #  широкоформатные размеры картинок
        #  Картинки должны сохранятся в следующей директории
        #  "номер_месяца/день_месяца": 08/22/img1.png, ...
        #  Подсказка: Модули os, from datetime import datetime, также метод
        #  strftime (можно и другой метод использовать)


main()
