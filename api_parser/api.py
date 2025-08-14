import requests
from bs4 import BeautifulSoup
from pprint import pprint

pokemons_names: dict = {}
for i in range(1, 3):
    pokemons_url: str = f"https://www.giantbomb.com/profile/wakka/lists/the-150-original-pokemon/59579/?page={i}"
    pokemons_response = requests.get(pokemons_url)
    soup = BeautifulSoup(pokemons_response.text, features="html.parser")
    pokemons = soup.find("ul", class_="editorial user-list js-simple-paginator-container")

    if pokemons:
        for li in pokemons:
            li = li.find_next("li")
            name_tag = li.find_next("h3")

            if name_tag:
                number_and_name = name_tag.text

                if number_and_name:
                    number_and_name = number_and_name.split(". ")
                    num, name = int(number_and_name[0]), number_and_name[1]

                    if num not in pokemons:
                        pokemons_names[num] = name
length: int = len(str(len(pokemons_names)))
for num, name in pokemons_names.items():
    print(f"{num:>{length}}. {name}")

[print() for _ in range(2)]

user_input: int = int(input("Choose the num of your favourite pokemon: "))

pokemon_name = pokemons_names[user_input]

url = (f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")


response = requests.get(url)


pokemon_info_name: dict = response.json().get("name").capitalize()

print(f"Pokemon name: {pokemon_info_name}")
print(f"{pokemon_info_name}s id: {response.json().get("id")}")
print(f"Height: {response.json().get("height")}")
print(f"Weight: {response.json().get("weight")}")

# pokemon_info: dict = response.json()
# pprint(pokemon_info)
# print(f"{pokemon_info['name']}")
# print(f"{pokemon_info['id']}")
# print(f"{pokemon_info['height']}")
# print(f"{pokemon_info['weight']}")
