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
        # достаю из списка первый элемен, он же уже не в списке, теперь это строка, почему Python считает, что это список?
        name = li.contents[0].strip()
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
    name = catalog[user_input][0]
    selected_url = catalog[user_input][1]

    [print() for i in range(2)]

    print(f"Выбрана категория: {name}  {selected_url} ")


response_2 = requests.get(selected_url)
category_2 = set(soup.find("ul", class_="wallpapers__list"))
print(response.status_code)
[print() for i in range(2)]

catalog_2: dict = {}

length_category_2 = len(str(len(category_2)))
selected_img_link: str = ""
if category_2:
    for i, li in enumerate(category_2, 1):

        a = li.find_next("a", class_="wallpapers__link")
        #a = li.find_next('img', class_="wallpapers__canvas")
        link = a.get("href")
        name = (a.find_next("img", class_="wallpapers__image").attrs['alt'].replace("Превью", "")).strip().capitalize()

        catalog_2[i] = [name, url + link]

        print(f"{i:>{length_category_2}}. {name}")

    [print() for i in range(2)]

    user_input_2 = int(input("Выберите номер картинки, подходящей по описанию: "))

    selected_img_name = catalog_2[user_input_2][0]
    selected_img_link = catalog_2[user_input_2][1]

    [print() for i in range(2)]
    print(f"Вы выбрали картинку '{selected_img_name} {selected_img_link}'")

# response_3 = requests.get(selected_img_link)
# soup = BeautifulSoup(response.text, features="html.parser")
# category_3 = soup.find("div", class_="gui-toggler__content JS-Toggler-Content")
# # print(response.status_code)
# # print(category_3)
#
# for div_ in category_3:
#     div_ = div_.find_next("div", class_="resolutions__title gui-h3")
#     print(div_)
#
#
#


    #
    #
    # with open("image.jpg", "wb") as i:
    #     i.write(response.content)
    #
    #
    #
    #







