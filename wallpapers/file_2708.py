import uuid
from pprint import pprint

import requests
from bs4 import BeautifulSoup

image_link = "https://wallpaperscraft.ru/wallpaper/golubianka_argus_rudbekiia_babochka_1428885"


# Неправильный подход идти по индексам
def first_approach():
    response = requests.get(image_link)
    soup = BeautifulSoup(response.text, features="html.parser")
    widescreen_resolutions = soup.find_all(
        "section",
        class_="resolutions__section resolutions__section_torn",
    )[-1].find_all("div", class_="resolutions__table")
    print(widescreen_resolutions)


# Универсальная функция
def get_resolutions_by_section(name: str = "Широкоформатные") -> dict[str, list[tuple[str, str]]]:
    response = requests.get(image_link)
    soup = BeautifulSoup(response.text, features="html.parser")
    sections = soup.find_all(
        "section",
        class_="resolutions__section resolutions__section_torn",
    )

    resolutions: dict[str, list[tuple[str, str]]] = {}
    for section in sections:
        curr_div = section.find("div", string=name)
        if curr_div:
            print(curr_div)
            all_resolutions_by_section = section.find_all(
                "div", class_="resolutions__table"
            )
            for resolution in all_resolutions_by_section:
                caption = resolution.find(
                    "div",
                    class_="resolutions__cell resolutions__caption",
                ).get_text()

                items = resolution.find_all(
                    "ul",
                    class_="resolutions__cell resolutions__list"
                )
                for item in items:
                    resolutions[caption] = resolutions.get(caption, [])
                    links = item.find_all("a", class_="resolutions__link")
                    resolutions[caption] = [
                        (link.get_text(), link.get("href"))
                        for link in links
                    ]

    # pprint(resolutions)
    return resolutions


get_resolutions_by_section("Полноэкранные")

# ---------------- Пример 1

counter = {}

s = "abaaacds"

for char in s:
    if char in counter:
        counter[char] += 1
    else:
        counter[char] = 1

    counter[char] = counter.get(char, 0) + 1

# ---------------- Пример 2

image_name = "Обои ducati"
curr_size = "1280x720"

unique_id: str = str(uuid.uuid4())

print(unique_id)

full_image_name = f"{image_name}_{unique_id}_{curr_size}"
print(full_image_name)
