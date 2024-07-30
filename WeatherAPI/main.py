import datetime as dt
import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = open("api_key", "r").read().strip()


def kelvin_to_celsius_fahrenheit(kelvin):
    celsius = kelvin - 273.15
    fahrenheit = celsius * (9 / 5) + 32
    return celsius, fahrenheit


def get_weather(city, api_key):
    url = BASE_URL + "appid=" + api_key + "&q=" + city
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if data.get("cod") != 200:
            print(f"Error al obtener el clima para {city}: {data.get('message')}")
            return None
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Error connecting: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    return None


def display_weather_info(city, data):
    if data:
        temp_kelvin = data["main"]["temp"]
        temp_celsius, temp_fahrenheit = kelvin_to_celsius_fahrenheit(temp_kelvin)
        feels_like_kelvin = data["main"]["feels_like"]
        feels_like_celsius, feels_like_fahrenheit = kelvin_to_celsius_fahrenheit(feels_like_kelvin)
        wind_speed = data["wind"]["speed"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        sunrise_time = dt.datetime.fromtimestamp(data["sys"]["sunrise"] + data["timezone"], dt.timezone.utc)
        sunset_time = dt.datetime.fromtimestamp(data["sys"]["sunset"] + data["timezone"], dt.timezone.utc)

        print(f"Temperature in {city}: {temp_celsius:.2f}°C or {temp_fahrenheit:.2f}°F")
        print(f"Feels like in {city}: {feels_like_celsius:.2f}°C or {feels_like_fahrenheit:.2f}°F")
        print(f"Humidity in {city}: {humidity}%")
        print(f"Wind Speed in {city}: {wind_speed} m/s")
        print(f"General Weather in {city}: {description}")
        print(f"Sun rises in {city} at {sunrise_time} local time.")
        print(f"Sun sets in {city} at {sunset_time} local time.")
    else:
        print(f"No se pudo obtener el clima para {city}")


def compare_weather(city_a, city_b, api_key):
    weather_data_a = get_weather(city_a, api_key)
    weather_data_b = get_weather(city_b, api_key)

    print(f"Clima en {city_a}:")
    display_weather_info(city_a, weather_data_a)

    print(f"\nClima en {city_b}:")
    display_weather_info(city_b, weather_data_b)


# Define the cities
city_a = "Panama"
city_b = "Costa Rica"

# Compare the weather between the two cities
compare_weather(city_a, city_b, API_KEY)
