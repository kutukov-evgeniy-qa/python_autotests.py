import requests

#Задаем переменные
url = 'https://api.pokemonbattle.ru/v2/'
header = {
    'trainer_token':'4e8b13cb6701938caf987e1967e9ab06',
    'Content-Type': 'application/json'
}  
body_create = {
    "name": "generate",
    "photo_id": -1
} 
#Первый запрос Создание покемона (POST /pokemons)
response_create = requests.post(url=f'{url}pokemons', headers=header, json=body_create)
print(response_create.status_code)
print(response_create.json()) #Выводим статус код и json ответа

pokemon = response_create.json()['id'] #сохраняем id созданного покемона в переменную для дальнейшего использования
body_rename = {
    "pokemon_id": pokemon,
    "name": "Pikachu",          #боди для второго запроса, записал его здесь, чтобы действовала переменная с id покемона
    "photo_id": -1
}  
#Второй запрос Смена имени покемона (PUT /pokemons)
response_rename = requests.put(url=f'{url}pokemons', headers=header, json=body_rename)
print(response_rename.status_code)
print(response_rename.json()) #Выводим статус код и json ответа

#Третий запрос Поймать покемона в покебол (POST /trainers/add_pokeball)
response_add_pok = requests.post(url=f'{url}trainers/add_pokeball', headers=header, json={"pokemon_id": pokemon})
print(response_add_pok.status_code)
print(response_add_pok.json()) #Выводим статус код и json ответа

#Четвертый запрос - подчищаем за собой, то есть удаляем покемона
response_knock = requests.post(url=f'{url}pokemons/knockout', headers=header, json={"pokemon_id": pokemon})
print(response_knock.status_code)
print(response_knock.json()) #Выводим статус код и json ответа