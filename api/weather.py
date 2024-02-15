import csv
import os
from datetime import datetime

import requests


def get_weather(location="Freiburg"):
    api_key = "874edd8d83674f1db8101409241502"
    api_url = f"https://api.weatherapi.com/v1/current.json?q={location}&key={api_key}"
    try:
        response = requests.get(api_url)
        data = response.json()
        if 'current' in data:
            weather_data = {
                'location': location,
                'temperature_c': data['current']['temp_c'],
                'condition': data['current']['condition']['text'],
                'wind_kph': data['current']['wind_kph'],
                'wind_dir': data['current']['wind_dir'],
                'pressure_mb': data['current']['pressure_mb'],
                'humidity': data['current']['humidity'],
                'cloud': data['current']['cloud'],
                'feelslike_c': data['current']['feelslike_c'],
                'visibility_km': data['current']['vis_km'],
            }
            save_weather_data(weather_data)
            return weather_data
        else:
            return {"error": "Unable to fetch weather data."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Request exception: {e}"}


def save_weather_data(weather_data):
    # Ensure the directory exists
    directory = "data/weatherdata"
    os.makedirs(directory, exist_ok=True)
    filename = os.path.join(directory, f"{weather_data['location'].lower().replace(' ', '_')}_weather_data.csv")

    with open(filename, mode='w', newline='') as file:  # Changed mode from 'a' to 'w'
        fieldnames = ['timestamp', 'location', 'temperature_c', 'condition', 'wind_kph', 'wind_dir', 'pressure_mb',
                      'humidity', 'cloud', 'feelslike_c', 'visibility_km']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()  # Write headers every time (since we're overwriting)

        # Add current timestamp with only the hour
        current_time = datetime.now().strftime('%H')  # Changed format to only include the hour
        weather_data['timestamp'] = current_time

        writer.writerow(weather_data)


def get_simplified_weather_info(location="Freiburg"):
    weather_data = get_weather(location)
    if 'error' not in weather_data:
        # Constructing a simplified weather information string
        simplified_info = (f"{weather_data['condition']}\n"
                           f"{weather_data['location']}: "
                           f"{weather_data['temperature_c']}°C")
        return simplified_info
    else:
        return weather_data['error']


def get_wind_and_pressure_info(location="Freiburg"):
    weather_data = get_weather(location)
    if 'error' not in weather_data:
        wind_and_pressure_info = (
            f"Wind Speed: {weather_data['wind_kph']} kph\n"
            f"Wind Direction: {weather_data['wind_dir']}\n"
            f"Pressure: {weather_data['pressure_mb']} mb"
        )
        return wind_and_pressure_info
    else:
        return weather_data['error']


def get_additional_weather_info(location="Freiburg"):
    weather_data = get_weather(location)
    if 'error' not in weather_data:
        additional_weather_info = (
            f"Cloud Cover: {weather_data['cloud']}%\n"
            f"Feels Like: {weather_data['feelslike_c']}°C\n"
            f"Visibility: {weather_data['visibility_km']} km"
        )
        return additional_weather_info
    else:
        return weather_data['error']
