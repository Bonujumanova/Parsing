import csv
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import time


main_url: str = "https://www.sima-land.ru/"
url: str = "https://www.sima-land.ru/novogodnie-ukrasheniya-dlya-doma/"

catalog: dict = {}
count: int = 0
for page in range(1, 11):
    curr_url = f"{url}p{page}"
    print(curr_url)
    response = requests.get(curr_url)
    soup = BeautifulSoup(response.text, features="html.parser")
    items = soup.find_all("div", class_="Tjryv6 jMV4W3 m5Eg__ catalog__item m358ND")

    if response:
        for index, div in enumerate(items, 1):
            count += 1
            link: str = main_url + div.find("a", class_="odeaio papCzt PfpX13").get("href")
            name: str = div.find_next("img").attrs['alt']
            wholesale_price: str = div.find_next("div", class_= "ziJG2p").find_next("span", class_="XJIe4q").text
            retail_price: str = div.find_next("div", class_="LBevbX").find_next("span", class_="XJIe4q").text
            rating: int = 5
            # rating: str = div.find_next("div", class_="e0qJYS").find_next("span", class_="jYoDfB")
            # if rating:
            #     rating = rating.title()
            #     print(rating)
            # else:
            #     rating = "Отзывов на товар пока нет"
            catalog[count] = {"name": name, "link":link, "wholesale_price":wholesale_price, "retail_price": retail_price, "rating":rating}

    time.sleep(2)


ENCODING: str = "UTF-8"
with open("data/goods.csv", "a", encoding=ENCODING) as csv_f:
    fieldnames = catalog[1].keys()
    print(fieldnames)
    writer = csv.DictWriter(csv_f,
                            fieldnames=fieldnames)
    writer.writeheader()  # Записываем заголовок

    for key_num in range(1, len(catalog) + 1):
        writer.writerow(catalog[key_num])  # Записываем строки


# catalog: dict = {
#     "1": {
#         "name": "\u0415\u043b\u043e\u0447\u043d\u0430\u044f \u0438\u0433\u0440\u0443\u0448\u043a\u0430 \u00ab\u0421\u0447\u0430\u0441\u0442\u043b\u0438\u0432\u044b\u0439 \u043c\u0430\u043b\u044b\u0448\u00bb, \u0431\u0435\u043b\u0430\u044f, \u041c\u0418\u041a\u0421",
#         "link": "https://www.sima-land.ru//3584586/elochnaya-igrushka-schastlivyy-malysh-belaya-miks/",
#         "wholesale_price": "86,92\u2009\u20bd",
#         "retail_price": "139\u2009\u20bd",
#         "rating": "5"
#     },
#     "2": {
#         "name": "\u041d\u0430\u043a\u043b\u0435\u0439\u043a\u0438 \u043d\u0430 \u043e\u043a\u043d\u0430 \u043d\u043e\u0432\u043e\u0433\u043e\u0434\u043d\u0438\u0435 \u00ab\u0421\u043d\u0435\u0436\u0438\u043d\u043a\u0438\u00bb, 12 \u0448\u0442., 9\u00d79 \u0441\u043c",
#         "link": "https://www.sima-land.ru//3816912/nakleyki-na-okna-novogodnie-snezhinki-12-sht-9-9-cm/",
#         "wholesale_price": "69,70\u2009\u20bd",
#         "retail_price": "85\u2009\u20bd",
#         "rating": "4.9"
#     },
#     "3": {
#         "name": "\u0421\u0432\u0435\u0442\u043e\u0434\u0438\u043e\u0434\u043d\u0430\u044f \u0444\u0438\u0433\u0443\u0440\u0430 \u043f\u043e\u0434 \u043a\u0443\u043f\u043e\u043b\u043e\u043c \u00ab\u0414\u043e\u043c\u0438\u043a\u00bb 6\u00d7 9.5 \u00d7 6 \u0441\u043c, \u0434\u0435\u0440\u0435\u0432\u043e, \u0431\u0430\u0442\u0430\u0440\u0435\u0439\u043a\u0438 LR1130\u04453 (\u0432 \u043a\u043e\u043c\u043f\u043b\u0435\u043a\u0442\u0435), \u0441\u0432\u0435\u0447\u0435\u043d\u0438\u0435 \u0442\u0451\u043f\u043b\u043e\u0435 \u0431\u0435\u043b\u043e\u0435",
#         "link": "https://www.sima-land.ru//6117395/svetodiodnaya-figura-pod-kupolom-domik-6-9-5-6-cm-derevo-batareyki-lr1130h3-v-komplekte-svechenie-teploe-beloe/",
#         "wholesale_price": "144,32\u2009\u20bd",
#         "retail_price": "253\u2009\u20bd",
#         "rating": "4.6"
#     },
#     "4": {
#         "name": "\u0421\u0443\u0432\u0435\u043d\u0438\u0440 \u043a\u0435\u0440\u0430\u043c\u0438\u043a\u0430 \u0441\u0432\u0435\u0442 \"\u041c\u0430\u043b\u044b\u0448\u043a\u0430 \u0432 \u0448\u0443\u0431\u043a\u0435 \u0438 \u0441 \u0440\u043e\u0436\u043a\u0430\u043c\u0438 \u043d\u0430 \u043a\u0430\u043f\u044e\u0448\u043e\u043d\u0435, \u0441\u043e \u0441\u043d\u0435\u0436\u043a\u043e\u043c\" 44\u044522\u044519 \u0441\u043c",
#         "link": "https://www.sima-land.ru//7567959/suvenir-keramika-svet-malyshka-v-shubke-i-s-rozhkami-na-kapyushone-so-snezhkom-44h22h19-cm/",
#         "wholesale_price": "2\u2009050\u2009\u20bd",
#         "retail_price": "3\u2009500\u2009\u20bd",
#         "rating": "4.2"
#     },
#     "5": {
#         "name": "\u0421\u0443\u0432\u0435\u043d\u0438\u0440 \u043a\u0435\u0440\u0430\u043c\u0438\u043a\u0430 \u0441\u0432\u0435\u0442 \"\u0421\u043d\u0435\u0433\u043e\u0432\u0438\u043a \u0441 \u043f\u0442\u0438\u0446\u0435\u0439 \u0438 \u0437\u0438\u043c\u043d\u0438\u043c \u0434\u043e\u043c\u0438\u043a\u043e\u043c, \u0441\u0440\u0435\u0437 \u0434\u0435\u0440\u0435\u0432\u0430\" 41\u044525\u04459 \u0441\u043c",
#         "link": "https://www.sima-land.ru//7567972/suvenir-keramika-svet-snegovik-s-pticey-i-zimnim-domikom-srez-dereva-41h25h9-cm/",
#         "wholesale_price": "1\u2009991,78\u2009\u20bd",
#         "retail_price": "3\u2009400\u2009\u20bd",
#         "rating": "5"
#     },
#     "6": {
#         "name": "\u0412\u0435\u0442\u043a\u0430 \u0434\u0435\u043a\u043e\u0440\u0430\u0442\u0438\u0432\u043d\u0430\u044f \u043d\u043e\u0432\u043e\u0433\u043e\u0434\u043d\u044f\u044f, 60 \u0441\u043c",
#         "link": "https://www.sima-land.ru//9690101/vetka-dekorativnaya-novogodnyaya-60-cm-2/",
#         "wholesale_price": "368,18\u2009\u20bd",
#         "retail_price": "579\u2009\u20bd",
#         "rating": "4.7"
#     },
#     "7": {
#         "name": "\u0414\u0435\u043a\u043e\u0440 \u0441\u0443\u0445\u043e\u0446\u0432\u0435\u0442 \u00ab\u0425\u043b\u043e\u043f\u043e\u043a\u00bb, h=30 \u0441\u043c, d=5 \u0441\u043c, \u0431\u0435\u043b\u044b\u0439",
#         "link": "https://www.sima-land.ru//2334965/dekor-suhocvet-hlopok-h-30-cm-d-5-cm-belyy/",
#         "wholesale_price": "15,99\u2009\u20bd",
#         "retail_price": "26,30\u2009\u20bd",
#         "rating": "4.9"
#     },
#     "8": {
#         "name": "\u041d\u0430\u043a\u043b\u0435\u0439\u043a\u0438 \u043d\u0430 \u043e\u043a\u043d\u0430 \u043c\u043d\u043e\u0433\u043e\u0440\u0430\u0437\u043e\u0432\u044b\u0435 \u00ab\u041d\u043e\u0432\u044b\u0439 \u0433\u043e\u0434\u00bb, \u0447\u0430\u0441\u044b, 33 \u0445 50 \u0441\u043c",
#         "link": "https://www.sima-land.ru//4921111/nakleyki-na-okna-mnogorazovye-novyy-god-chasy-33-h-50-cm/",
#         "wholesale_price": "56,58\u2009\u20bd",
#         "retail_price": "85\u2009\u20bd",
#         "rating": "5"
#     },
#     "9": {
#         "name": "\u041d\u0430\u043a\u043b\u0435\u0439\u043a\u0438 \u043d\u0430 \u043e\u043a\u043d\u0430 \u043c\u043d\u043e\u0433\u043e\u0440\u0430\u0437\u043e\u0432\u044b\u0435 \u00ab\u0421 \u041d\u043e\u0432\u044b\u043c \u0433\u043e\u0434\u043e\u043c\u00bb, \u0441\u043d\u0435\u0433\u0438\u0440\u0438, 33 \u0445 50 \u0441\u043c",
#         "link": "https://www.sima-land.ru//4273357/nakleyki-na-okna-mnogorazovye-s-novym-godom-snegiri-33-h-50-cm/",
#         "wholesale_price": "56,58\u2009\u20bd",
#         "retail_price": "85\u2009\u20bd",
#         "rating": "4.9"
#     },
#     "10": {
#         "name": "\u0415\u043b\u043e\u0447\u043d\u0430\u044f \u0438\u0433\u0440\u0443\u0448\u043a\u0430 \u00ab\u0412\u0435\u0441\u0451\u043b\u0430\u044f \u043b\u043e\u0448\u0430\u0434\u043a\u0430\u00bb",
#         "link": "https://www.sima-land.ru//1032654/elochnaya-igrushka-veselaya-loshadka/",
#         "wholesale_price": "31,98\u2009\u20bd",
#         "retail_price": "59\u2009\u20bd",
#         "rating": "4.8"
#     }
# }

