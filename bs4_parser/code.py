import requests

from bs4 import BeautifulSoup

url: str = "https://wallpaperscraft.ru/"

response = requests.get(url)

print(response.status_code)

soup = BeautifulSoup(response.text, features="html.parser")

category = soup.find("ul", class_="filters__list JS-Filters")

category_name_and_link: dict[str, str] = {}
selected_url: str = ""

if category:
    for li in category:
        li = li.find_next("a", class_="filter__link")
        name: str = li.contents[0].strip()
        link = li.get("href")
        if name:
            category_name_and_link[name] = url + link

    length_category: int = len(str(len(category_name_and_link)))
    catalog: dict[int, list[str]] = {}
    for i, category_name_items in enumerate(category_name_and_link.items(), 1):
        print(f"{i:>{length_category}}. {category_name_items[0]}")

        name = category_name_items[0]
        link = category_name_items[1]
        catalog[i] = [name, link]


    user_input: int = int(input("Выберите номер категории: "))
    name:str = catalog[user_input][0]
    selected_url: str = catalog[user_input][1]

    print(f"Выбрана категория: {name}  {selected_url}\n\n")

response_2 = requests.get(selected_url)
soup = BeautifulSoup(response_2.text, features="html.parser")
category_2 = set(soup.find("ul", class_="wallpapers__list"))

catalog_2: dict = {}
length_category_2 = len(str(len(category_2)))
selected_img_link: str = ""

if category_2:
    for i, li in enumerate(category_2, 1):
        a = li.find_next("a", class_="wallpapers__link")
        link = a.get("href")
        name = (a.find_next("img", class_="wallpapers__image").attrs['alt'].replace("Превью", "")).strip().capitalize()
        catalog_2[i] = [name, url + link]
        print(f"{i:>{length_category_2}}. {name}")

    user_input_2 = int(input("\n\nВыберите номер картинки, подходящей по описанию: "))

    selected_img_name: str = catalog_2[user_input_2][0]
    selected_img_link: str = catalog_2[user_input_2][1]

    print(f"\n\nВы выбрали картинку '{selected_img_name} {selected_img_link}'")

response_3 = requests.get(selected_img_link)
soup = BeautifulSoup(response_3.text, features="html.parser")
category_3 = soup.find("span", class_="wallpaper-table__cell")

wallpaper_link: str = ""

for a in category_3:
    a = a.find_next("a")
    wallpaper_link = url + a.get("href")

response_4 = requests.get(wallpaper_link)
soup = BeautifulSoup(response_4.text, features="html.parser")
category_4 = soup.find("div", class_="gui-toolbar__item gui-hidden-mobile")

a = category_4.find("a", class_="gui-button gui-button_full-height")
finally_download_link: str = a.get("href")

if finally_download_link:
    response_4 = requests.get(finally_download_link)
    with open("images/image.jpg", "wb") as i:
        i.write(response_4.content)
