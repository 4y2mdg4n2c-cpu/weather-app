import requests
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")
def get_weather(name):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={name}&appid={api_key}&units=metric&lang=ru"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("Запрос превысил время ожидания(10 секунд). Пожалуйста, попробуйте позже.")
        return None
    except requests.exceptions.HTTPError as err:
        status_code = err.response.status_code
        if status_code == 404:
            print("Город не найден. Пожалуйста, проверьте правильность ввода и попробуйте снова.")
            return None
        elif status_code == 401:
            print("Неверный API ключ. Пожалуйста, проверьте его и попробуйте снова.")
            return None
        else:   
            print(f"HTTP ошибка: {status_code}. Пожалуйста, попробуйте позже.")
            return None
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return None
def results_weather(data):
    city = data['name']
    temp = data['main']['temp']
    country = data['sys']['country']
    wind_speed = data['wind']['speed']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    description = data['weather'][0]['description']
    results = {
    "Страна": country,
    "Город": city,
    "Температура": f"{temp}°C",
    "Ощущается как": f"{feels_like}°C",
    "Скорость ветра": f"{wind_speed} м/с",
    "Влажность": f"{humidity}%",
    "Погодные условия": description}
    return results
while True:
    name = input('Введите название города ("exit" для выхода): ')
    if name == 'exit'.lower():
        print(f'Выход...')
        break
    data = get_weather(name)
    if data is None:
        continue
    result_weather = results_weather(data)
    for key, value in result_weather.items():
        print(f"{key}: {value}")