import datetime
import os
import time
import uuid

from pprint import pprint

import requests
from bs4 import BeautifulSoup

from wallpapers.constants import CATEGORIES_MAP, SITE_URL


def show_categories(categories: dict[str, str]) -> None:
    for num, categories_name in enumerate(categories.keys(), 1):
        print(f"{num}. {categories_name}")


def show_images(data: dict[str, list]) -> None:
    length: int = len(str(len(data)))
    for number, value in enumerate(data.values(), 1):
        print(f"{number:>{length}}. {' '.join(value)}")


# TODO: Пересмотреть название функции.
def get_selected_img(
        images: dict[str, list],numbers: list[int], url: str
) -> dict[str, list]:
    selected_images: dict[str, list] = {}
    for number in numbers:
        image_link = list(images.keys())[number - 1]
        image_name = images.get(image_link)
        selected_images[url + image_link] = image_name

    return selected_images



def get_resolutions_by_section(name: str = "Широкоформатные", image_link: str= "")\
        -> dict[str, list[tuple[str, str]]]:
    response = requests.get(image_link)

    soup = BeautifulSoup(response.text, features="html.parser")
    sections = soup.find_all(
        'section',
        class_='resolutions__section resolutions__section_torn'
        )

    resolutions: dict[str, list[tuple[str, str]]] = {}
    for section in sections:
        curr_div = section.find('div', string=name)
        if curr_div:

            all_resolutions_by_section = section.find_all(
                'div', class_='resolutions__table'
            )
            for resolution in all_resolutions_by_section:
                caption = resolution.find(
                    'div',
                    class_='resolutions__cell resolutions__caption'
                ).get_text()

                items = resolution.find_all(
                    'ul',
                    class_='resolutions__cell resolutions__list'
                )
                for item in items:
                    resolutions[caption] = resolutions.get(caption, [])
                    links = item.find_all('a', class_='resolutions__link')
                    resolutions[caption] = [
                        (link.get_text(), link.get('href'))
                        for link in links
                    ]
    return resolutions


def show_img_captions(captions_and_resolutions: dict) -> None:
    for num, caption in enumerate(captions_and_resolutions.keys(), 1):
        print(f"{num}. {caption}")


def show_selected_caption_resolutions(captions_and_resolutions: dict, number) -> list[tuple]:
    selected_caption = list(captions_and_resolutions.values())[number - 1]
    for num, image in enumerate(selected_caption, 1):
        size, _ = image
        print(f"{num}. SIZE: {size}")
    return selected_caption

def download_selected_image(selected_caption, selected_img_num, main_url, img_name) -> None:
    img_size, img_link = selected_caption[selected_img_num - 1]

    response = requests.get(main_url + img_link)
    soup = BeautifulSoup(response.text, features="html.parser")
    link_for_downloading = soup.find(
        'a',
        class_='gui-button gui-button_full-height'
    ).get('href')
    response = requests.get(link_for_downloading)


    year, month, day = datetime.date.today().isoformat().split("-")
    unique_id: str = str(uuid.uuid4())
    curr_name = f"{img_name}_{unique_id}_{img_size}"

    os.makedirs(f'{year}/{month}/{day}', exist_ok=True)
    with open(f"{year}/{month}/{day}/{curr_name}.jpg", "wb") as f:
        f.write(response.content)


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
    images_and_links: dict[str, list] = {}

    for page_num in range(1, 2):
        curr_page: str = get_category_page(category_link, page_num)
        parse_images_on_page(curr_page, images_and_links)
        for i in range(10, 0, -1):
            print(f"\rLoading {i}...", end="")
            time.sleep(1)
    print()
    show_images(images_and_links)

    # TODO: название переменной
    count_images: int = len(images_and_links)

    selected_images_nums: list[int] = []
    print("\nSelect image number. Press 'q' to complete the input\n")
    choice_image_number = input()
    if choice_image_number.isdigit():
        selected_images_nums.append(int(choice_image_number))

    while choice_image_number.lower() != 'q':
        choice_image_number = input()
        if choice_image_number == 'q':
            break
        if not choice_image_number.isdigit():
            print("Enter a integer number")
            continue
        elif not (1 <= int(choice_image_number) <= count_images):
            break
        else:
            selected_images_nums.append(int(choice_image_number))
    selected_main_url: str = SITE_URL[choice_lang]
    images_names_and_links = get_selected_img(
        images_and_links, selected_images_nums, selected_main_url
    )

    for image_link, image_name in images_names_and_links.items():

        captions_and_resolutions = get_resolutions_by_section("Широкоформатные", image_link)

        for i in range(10, -1, -1):
            print(f"\rLoading {'*' * i}...", end="")
            time.sleep(1)
        print()
        show_img_captions(captions_and_resolutions)

        print(f"\nChoose caption for image '{image_name[0]}'")

        caption_number = int(input())

        selected_caption = show_selected_caption_resolutions(
            captions_and_resolutions, caption_number
        )

        print(f"\nSelect resolution for image")
        num_selected_resolution = int(input())

        download_selected_image(
            selected_caption,
            num_selected_resolution,
            selected_main_url,
            image_name[0]
        )


main()
