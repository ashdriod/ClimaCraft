import requests
import csv
import os


def fetch_weather_data(location="Freiburg"):
    api_key = "f201b82ab7bf4b77974102847243101"
    api_url = f"https://api.weatherapi.com/v1/forecast.json?q={location}&days=7&key={api_key}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


def save_weather_data_to_csv(weather_data, file_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Open a CSV file to write
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["Time", "Temperature (C)", "Chance of Rain (%)", "Condition"])

        # Extract and write data for each hour in the forecast
        for forecast in weather_data["forecast"]["forecastday"]:
            for hour in forecast["hour"]:
                time = hour["time"]
                temp_c = hour["temp_c"]
                chance_of_rain = hour["chance_of_rain"]
                condition = hour["condition"]["text"]
                writer.writerow([time, temp_c, chance_of_rain, condition])

    print(f"Data successfully written to {file_path}")


if __name__ == "__main__":
    location = "Freiburg"
    weather_data = fetch_weather_data(location)

    if weather_data:
        file_path = "data/weatherdata/weather_data.csv"
        save_weather_data_to_csv(weather_data, file_path)
