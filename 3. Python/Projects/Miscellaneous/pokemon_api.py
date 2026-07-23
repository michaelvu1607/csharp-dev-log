import requests

BASE_URL = "https://pokeapi.co/api/v2/"

def get_poke_info(pokemon_name):
    url = f"{BASE_URL}/pokemon/{poke_name}"
    response = requests.get(url)
    if response.status_code == 200:
        poke_data = response.json()
        return poke_data
    else:
        print(f"Failed to retrieve data. {response.status_code}")

poke_name = "pikachu"
poke_info = get_poke_info(poke_name)

if poke_info:
    print(f"Name: {poke_info['name'].title()}")
    print(f"ID: {poke_info['id']}")
