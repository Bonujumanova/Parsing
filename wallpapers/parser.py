import datetime
import os
import time
import uuid
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup

from wallpapers.constants import CATEGORIES_MAP, SITE_URL


def get_page(link: str, parser: str = "html.parser") -> BeautifulSoup:
    response = requests.get(link)
    soup = BeautifulSoup(response.text, features=parser)

    return soup


def show_ordered_items(data: dict[str, Any]) -> None:
    for num, key in enumerate(data.keys(), 1):
        print(f"{num}. {key}")


def show_images(data: dict[str, list]) -> None:
    length: int = len(str(len(data)))
    for number, value in enumerate(data.values(), 1):
        print(f"{number:>{length}}. {' '.join(value)}")


def get_selected_img(
        images: dict[str, list], numbers: list[int]
) -> dict[str, list]:
    links: list[str] = list(images.keys())

    return {
        links[number - 1]: images.get(links[number - 1])
        for number in numbers
    }


def get_resolutions_by_section(
        image_link: str,
        section_name: str = "Широкоформатные",
) -> dict[str, list[tuple[str, str]]]:
    soup = get_page(image_link)

    sections = soup.find_all(
        'section',
        class_='resolutions__section resolutions__section_torn'
    )
    resolutions: dict[str, list[tuple[str, str]]] = {}
    for section in sections:
        curr_div = section.find('div', string=section_name)
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


def show_selected_image_info(
        data: dict[str, list[tuple[str, str]]],
        number: int
) -> list[tuple[str, str]]:
    selected_caption = list(data.values())[number - 1]
    for index, image in enumerate(selected_caption, start=1):
        resolution, _ = image
        print(f"{index}. Resolution: {resolution}")
    return selected_caption


def get_path() -> str:
    year, month, day = datetime.date.today().isoformat().split("-")
    file_path = os.path.join("images", year, month, day)
    os.makedirs(file_path, exist_ok=True)

    return file_path


def save_image(content: bytes, filename: Optional[str] = None) -> None:
    if filename is None:
        filename = str(uuid.uuid4())

    file_path = get_path()
    with open(f"{os.path.join(file_path, filename)}.jpg", "wb") as f:
        f.write(content)


def download_selected_image(
        selected_caption: list[tuple[str, str]],
        selected_img_num: int,
        site_base_url: str,
        img_name: str
) -> None:
    resolution, img_link = selected_caption[selected_img_num - 1]
    soup = get_page(site_base_url + img_link)
    download_link = soup.find(
        'a',
        class_='gui-button gui-button_full-height'
    ).get('href')
    response = requests.get(download_link)

    curr_name = f"{img_name}_{uuid.uuid4()}_{resolution}"
    save_image(response.content, filename=curr_name)


def parse_images_on_page(
        curr_page: str, all_images_data: dict[str, list]
) -> dict[str, list]:
    soup = BeautifulSoup(curr_page, features="html.parser")
    images = set(soup.find("ul", class_="wallpapers__list"))

    for li in images:
        item = li.find_next("a", class_="wallpapers__link")
        link = item.get("href")
        preview = item.find_next(
            "img",
            class_="wallpapers__image"
        ).attrs.get("alt", "Not previews").split(", ")
        all_images_data[link] = preview

    return all_images_data


def get_category_pagination_page(link: str, page_num: int) -> str:
    response = requests.get(f"{link}/page{page_num}/")

    if response.status_code == 200:
        return response.text

    if response.status_code == 404:
        raise ValueError("Page not found")

    raise ValueError("Something wrong")


def countdown_loader(delay: int, **kwargs) -> None:
    for i in range(delay, -1, -1):
        print(f"\rLoading {i}...", end="")
        time.sleep(1)

    if kwargs.get("additional", True):
        print("\rDone!\n", end="")
    else:
        print("\r", end="")

def preprocess_categories_map(lang: str, base_url: str) -> dict[str, str]:
    base_url: str = SITE_URL[lang]

    categories: dict[str, str] = {}
    for url, names in CATEGORIES_MAP.items():
        name = names.get(lang)
        categories[name] = base_url + url

    return categories
def main() -> None:
    max_page: int = 1

    choice_lang = input("Choice language (en, ru): ").lower()
    if choice_lang not in ("en", "ru"):
        raise ValueError("Unavailable language")

    base_url: str = SITE_URL[choice_lang]
    categories = CATEGORIES_MAP.get(choice_lang)
    categories = preprocess_categories_map(choice_lang, base_url)


    show_ordered_items(categories)

    selected_category_num: int = int(input("Select category number: "))
    if not (1 <= selected_category_num <= len(categories)):
        raise ValueError("Unavailable category")

    category_name = list(categories.keys())[selected_category_num - 1]
    category_link = categories.get(category_name)
    print(f"Selected category '{category_name}' - {category_link}")

    images_data: dict[str, list] = {}
    for page_num in range(1, max_page + 1):
        print(f"Parse page {page_num}")
        curr_page: str = get_category_pagination_page(category_link,
                                                      page_num)
        parse_images_on_page(curr_page, images_data)
        countdown_loader(3)

    print()
    show_images(images_data)

    selected_images_nums: list[int] = []
    print("\nSelect image number. Press 'q' to complete the input\n")

    # TODO: Баг: Если ввести неверный номер картинки программа
    #  не выводит соответствующую информацию.
    # Решила добавить флаг, тк пришлось бы делать проверку для самого первого ввода

    flag: bool = True
    while flag:
        choice_image_number = input()
        if choice_image_number.lower() == 'q':
            break
        if not choice_image_number.isdigit():
            print("Enter a integer number")
            continue
        elif int(choice_image_number) not in range(1, len(images_data) + 1):
            print(f"This picture doesn't exists. Select an image number from 1 to {len(images_data)}")
        else:
            selected_images_nums.append(int(choice_image_number))

    images_links_and_names = get_selected_img(images_data, selected_images_nums)
    for link, name in images_links_and_names.items():
        captions_and_resolutions = get_resolutions_by_section(base_url + link)
        countdown_loader(5, additional=False)
        print()
        show_ordered_items(captions_and_resolutions)

        preview, *_ = name
        print(f"\nChoose caption for image '{preview}'")

        caption_number = int(input())
        selected_caption = show_selected_image_info(
            captions_and_resolutions, caption_number
        )

        print(f"\nSelect resolution for image")
        num_selected_resolution = int(input())

        download_selected_image(
            selected_caption,
            num_selected_resolution,
            base_url,
            name[0]
        )
        print("Success!")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(f"Connection error with {SITE_URL}")
    except ValueError as e:
        print(f"Invalid data: {e}")
