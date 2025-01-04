import requests

URL = 'https://api.pokemonbattle.ru/v2/'
header = {
    'trainer_token':'f79e0e23bfdc841f501641794b8784e7',
    'Content-Type': 'application/json'
}  
body_create = {
    "name": "generate",
    "photo_id": -1
} 
trainer_id = '22397'

fight = True            #СТАРТУЕМ ЦИКЛ КОТОРЫЙ БУДЕТ 1.СОЗДАВАТЬ ПОКЕМОНА 2.ЛОВИТЬ ЕГО В ПОКЕБОЛ 3.ПРОВОДИТЬ БИТВУ ПОКА ПОКЕМОН НЕ УМРЕТ ИЛИ НЕ ДОСТИГНЕТ АТАКИ 7
while fight == True:    #БУДЕТ ПОВТОРЯТЬ ЭТИ ДЕЙСТВИЯ ПОКА НЕ ДОСТИГНЕМ ЛИМИТА БОЕВ ИЛИ НЕ ДОСТИГНЕМ ПОКЕМОНОМ АТАКИ 7
    #Создаем покемона
    response_create = requests.post(url=f'{URL}pokemons', headers=header, json=body_create)
    print(response_create.status_code)
    print(response_create.json())

    #Записываем id покемона
    pokemon_id = response_create.json()['id']

    #Ловим покемона в покебол
    response_catch = requests.post(url=f'{URL}trainers/add_pokeball',headers=header, json={"pokemon_id": pokemon_id})
    print(response_catch.status_code)
    print(response_catch.json())

    #Деремся на смерть
    battle = True
    while battle == True:
        enemy = False   #ВВОДИМ ЦИКЛ ЧТОБЫ НЕ ПОПАСТЬСЯ НА САМОГО СЕБЯ ПРИ ПОИСКЕ ПРОТИВНИКА
        i = 0           
        while enemy == False:
            response_enemy = requests.get(url= f'{URL}pokemons', params={'in_pokeball':1, 'sort':'asc_attack'}) #Ищем противника
            enemy_id = response_enemy.json()['data'][i]['id']   #ЗАПИСЫВАЕМ В ПЕРЕМЕННУЮ АЙДИ ПОКЕМОНА ИЗ ПЕРВОГО ОБЪЕКТА В МАССИВЕ (i = 0) 
            if response_enemy.json()['data'][i]['trainer_id'] != trainer_id:    #ЕСЛИ АЙДИ ТРЕНЕРА НАЙДЕННОГО ПОКЕМОНА НЕ РАВЕН НАШЕМУ, ТО ЕСТЬ НЕ ДЕРЕМСЯ С САМИМ СОБОЙ, ТОГДА ЗАКАНЧИВАЕМ ЦИКЛ
                enemy = True
            else: i += 1        #ЕСЛИ МЫ ПОПАЛИ НА САМОГО СЕБЯ, ТО УВЕЛИЧИВАЕМ i на 1 И ПРОВЕРЯЕМ СЛЕДУЮЩЕГО ПОКЕМОНА В МАССИВЕ, ПОКА НЕ НАЙДЕМ ПОДХОДЯЩЕГО
        response_battle = requests.post(url=f'{URL}battle', headers=header, json={"attacking_pokemon": pokemon_id, "defending_pokemon": enemy_id}) #ДЕРЕМСЯ
        response_battle_pokemon = requests.get(url=f'{URL}pokemons', params={'pokemon_id': pokemon_id})  #ВСПОМОГАТЕЛЬНЫЕ ДАННЫЕ ПО НАШЕМУ ПОКЕМОНУ (ЧТОБЫ ЗАВЕРШИТЬ ЦИКЛ, ЕСЛИ У НЕГО АТАКА 7)
        print(response_battle.status_code)
        print(response_battle.json())       #ПЕЧАТАЕМ ДАННЫЕ ПО БОЯМ
        if response_battle.json()['result'] == 'Твой покемон проиграл' or response_battle_pokemon.json()['data'][0]['attack'] == 7 or response_battle.json()['battle_limit'] == '50 из 50':
            battle = False      #ЕСЛИ ПОКЕМОН ПРОИГРАЛ, ДОСТИГ АТАКИ 7 или достигнут лимит боев 50, ТО ЗАВЕРШАЕМ ЦИКЛ))

    if response_battle_pokemon.json()['data'][0]['attack'] == 7 or response_battle.json()['battle_limit'] == '50 из 50':
        fight = False   #ЗАВЕРШАЕМ ЦИКЛ ЕСЛИ ДОСТИГЛИ АТАКИ 7 ИЛИ ДОСТИГНУТ ЛИМИТ БОЕВ

#ПОСЛЕ ВСЕХ БОЕВ СМОТРИМ НА НАШИХ ПОКЕМОНОВ)
pokemons = requests.get(url=f'{URL}trainers', params={'trainer_id': trainer_id}) #ОТПРАВЛЯЕМ ЗАПРОС НА ПОЛУЧЕНИЕ ДАННЫХ О НАШЕМ ТРЕНЕРЕ
print('СПИСОК ПОКЕМОНОВ В ПОКЕБОЛЕ', pokemons.json()['data'][0]['pokemons_in_pokeballs'])  #ВЫВОДИМ ДАННЫЕ ПО НАШИМ ПОКЕМОНАМ В ПОКЕБОЛАХ

#ЕСЛИ ВЫПАДАЕТ ОШИБКА, ТО СКОРЕЕ ВСЕГО ЗАКОНЧИЛИСЬ ПОКЕМОНЫ НА САЙТЕ