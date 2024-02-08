# api/weather.py
import requests

def get_weather(location="Freiburg"):
    api_key = "f201b82ab7bf4b77974102847243101"
    api_url = f"https://api.weatherapi.com/v1/current.json?q={location}&key={api_key}"
    try:
        response = requests.get(api_url)
        data = response.json()
        if 'current' in data:
            temperature = data['current']['temp_c']
            condition = data['current']['condition']['text']
            weather_info = f"Weather in {location}: {condition}, Temperature: {temperature}°C"
            return weather_info
        else:
            return "Error: Unable to fetch weather data."
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "Error: Unable to fetch weather data."
