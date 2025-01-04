import requests
import pytest

#Задаем переменные
url = 'https://api.pokemonbattle.ru/v2/'
header = {
    'trainer_token':'4e8b13cb6701938caf987e1967e9ab06',
    'Content-Type': 'application/json'
}  
trainer_id = '13698'    #id тренера
trainer_name = 'kimich' #имя тренера

# Тест на проверку статус кода ответа запроса GET /v2/trainers [Получение списка тренеров]
def test_get_trainers_status():
    response_status = requests.get(url=f'{url}trainers') #отправляем запрос
    assert response_status.status_code == 200            #проверяем статус код

#Проверка, что в ответе приходит строчка с именем моего тренера
def test_get_trainers_name():
    response_name = requests.get(url=f'{url}trainers', params={'trainer_id':trainer_id}) #отправляем запрос с квери параметром trainer_id для поиска моего тренера
    assert response_name.json()['data'][0]['trainer_name'] == trainer_name              #обращаемся к ключу trainer_name и проверяем что он совпадает с заданной переменной

#Пробую параметризацию на запросе GET /v2/trainers [Получение списка тренеров]
@pytest.mark.parametrize('key, value', [('id', trainer_id),('level', '5'),('city', 'Moscow')]) #задаем переменные для перебора в тестах
def test_parametrize(key, value):  #указываем переменные в тесте
    response_parametrize = requests.get(url=f'{url}trainers', params={'trainer_id':trainer_id}) #отправляем запрос с квери параметром trainer_id для поиска моего тренера
    assert response_parametrize.json()['data'][0][key] == value #обращаемся к ключам из переменной key и сверяем их со значениями из переменной value