import time
from datetime import datetime
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from wallpapers.constants import CATEGORIES_MAP, SITE_URL


def show_categories(categories: dict[str, str]) -> None:
    # TODO: Реализовать вывод пронумерованных категорий
    pass


def show_images(data: dict[str, list]) -> None:
    length: int = len(str(len(data)))
    for number, value in enumerate(data.values(), 1):
        print(f"{number:>{length}}. {' '.join(value)}")
    # TODO: Реализовать вывод пронумерованных картинок:
    #  - Название
    #  - Ключевые слова
    #  - Абсолютная ссылка


# TODO: Пересмотреть название функции.
def get_image(
        images: dict[str, list],numbers: list[int], url: str
) -> dict[str, list]:
    selected_images: dict[str, list] = {}
    for number in numbers:
        image_link = list(images.keys())[number - 1]
        image_name = images.get(image_link)
        selected_images[url + image_link] = image_name

    return selected_images


def get_image_resolution(image_link: str):
    print(image_link)  # DEBUG

    response = requests.get(image_link)
    soup = BeautifulSoup(response.text, features="html.parser")
    widescreen_resolutions = soup.find_all(
        "div",
        class_="resolutions__title gui-h3",
        string="Широкоформатные"
    )
    print(widescreen_resolutions)
    # Не понимаю как же найти ссылку на конкретное разрешение..... В разрешениях для телефона, apple /
    # используются одинаковые названия+
    for li in widescreen_resolutions:
        # Вот тут ниже в поиске - ошибка, тк в print(f"a.contents === {a.contents}") выводятся только
        # первые элементы подзаголовков. Нужно искать по другому
        a = (li.find_next("div",
                          class_="resolutions__cell resolutions__caption").find_next
             ("a", class_="resolutions__link"))
        if a:
            print(f"a.contents === {a.contents}")
            if a.contents == '1920x1080' or a.contents == ["1920x1080"]:
                link: str = a.get("href")
                return link
    return "Такого разрешения нет"


# def download_image(img_link, url):
#     response = requests.get(url + img_link)
#     soup = BeautifulSoup(response.text, features="html.parser")
#
#     a = img_link.find_all("a", class_="gui-button gui-button_full-height")
#     finally_download_link: str = a.get("href")
#     print(f"download_image: {finally_download_link}")
#
#     if finally_download_link:
#         response = requests.get(finally_download_link)
#         with open("images/ssss.png", "ab+") as f:
#             f.write(response.content)


def parse_images_on_page(curr_page: str, all_images_names_and_links) -> dict[str, list]:
    soup = BeautifulSoup(curr_page, features="html.parser")
    all_images = set(soup.find("ul", class_="wallpapers__list"))

    # data: dict[str, list] = {}
    for i, li in enumerate(all_images, 1):
        item = li.find_next("a", class_="wallpapers__link")
        link = item.get("href")
        preview = item.find_next(
            "img",
            class_="wallpapers__image"
        ).attrs.get("alt", "Not previews").split(", ")
        all_images_names_and_links[link] = preview

    return all_images_names_and_links


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
    all_images_names_and_links: dict[str, list] = {}

    for page_num in range(1, 2):
        curr_page: str = get_category_page(category_link, page_num)
        # TODO: Не используется?
        images_on_page: dict[str, list] = parse_images_on_page(curr_page, all_images_names_and_links)

        for i in range(10, 0, -1):
            print(f"\rLoading {i}...", end="")
            time.sleep(1)

    show_images(all_images_names_and_links)

    # TODO: название переменной
    images_length: int = len(all_images_names_and_links)

    selected_images_nums: list[int] = []
    print("Select image number. Press 'q' to complete the input")
    choice_image_number = input()
    while choice_image_number.lower() != 'q':
        choice_image_number = input()

        if not choice_image_number.isdigit():
            print("Enter a integer number")
            continue

        if not (1 <= int(choice_image_number) <= images_length):
            break
        else:
            selected_images_nums.append(int(choice_image_number))
    url: str = SITE_URL[choice_lang]
    images_names_and_links = get_image(all_images_names_and_links, selected_images_nums, url)

    for image_link, image_name in images_names_and_links.items():
        img_lnk_for_dwnldng = get_image_resolution(image_link)
        print("img_lnk_for_dwnldng", img_lnk_for_dwnldng)
        # if img_lnk_for_dwnldng:
        #
        #     download_image(img_lnk_for_dwnldng, url)
        #

    # В этом случае важно обратить внимание на то, что возвращает get_image()
    # if choice_lang == 'en':
    #        image_link = SITE_URL['en'] + image_link
    # else:
    #     image_link = SITE_URL['ru'] + image_link
    # print(f"Selected category '{' '.join(image_name)}' - {image_link}")
    #
    #

    # for page_num in range(1, 5):
    #     curr_page: str = get_category_page(category_link, page_num)
    #
    #
    #     images_on_page: dict[str, list] = parse_images_on_page(curr_page)
    #     print(len(images_on_page))
    #     time.sleep(10)

    # TODO: Доработать логику выбора картинки, скачать все
    #  широкоформатные размеры картинок
    #  Картинки должны сохранятся в следующей директории
    #  "номер_месяца/день_месяца": 08/22/img1.png, ...
    #  Подсказка: Модули os, from datetime import datetime, также метод
    #  strftime (можно и другой метод использовать)


main()
