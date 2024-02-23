import csv
import os
from datetime import datetime
import requests

def fetch_weather_data(location="Freiburg"):
    api_key = "874edd8d83674f1db8101409241502"
    api_url = f"https://api.weatherapi.com/v1/forecast.json?q={location}&days=7&key={api_key}"

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # This will raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def save_weather_data_to_csv(weather_data, file_path):
    # Check if the file exists and read the first data row to check the date
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            first_row = next(reader, None)  # Get the first data row

            if first_row:
                first_row_date_str = first_row["Time"].split(" ")[0]  # Extract date part
                first_row_date = datetime.strptime(first_row_date_str, "%Y-%m-%d").date()
                today_date = datetime.now().date()

                if first_row_date == today_date:
                    print("Weather data is already up to date for today.")
                    return  # Exit the function if the data is already up to date

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Open a CSV file to write
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow([
            "Time", "Temperature (C)", "Temperature (F)", "Is Day", "Condition Text",
            "Condition Icon", "Condition Code", "Wind MPH", "Wind KPH", "Wind Degree",
            "Wind Direction", "Pressure MB", "Pressure IN", "Precipitation MM",
            "Precipitation IN", "Snow CM", "Humidity", "Cloud", "Feels Like (C)",
            "Feels Like (F)", "Wind Chill (C)", "Wind Chill (F)", "Heat Index (C)",
            "Heat Index (F)", "Dew Point (C)", "Dew Point (F)", "Will It Rain",
            "Chance of Rain", "Will It Snow", "Chance of Snow", "Visibility KM",
            "Visibility Miles", "Gust MPH", "Gust KPH", "UV", "Solar Radiation",
            "Diffuse Radiation"
        ])

        # Extract and write data for each hour in the forecast
        for forecast in weather_data["forecast"]["forecastday"]:
            for hour in forecast["hour"]:
                writer.writerow([
                    hour["time"], hour["temp_c"], hour["temp_f"], hour["is_day"],
                    hour["condition"]["text"], hour["condition"]["icon"], hour["condition"]["code"],
                    hour["wind_mph"], hour["wind_kph"], hour["wind_degree"],
                    hour["wind_dir"], hour["pressure_mb"], hour["pressure_in"], hour["precip_mm"],
                    hour["precip_in"], hour.get("snow_cm", 0), hour["humidity"], hour["cloud"],
                    hour["feelslike_c"], hour["feelslike_f"], hour.get("windchill_c", ""),
                    hour.get("windchill_f", ""), hour.get("heatindex_c", ""), hour.get("heatindex_f", ""),
                    hour["dewpoint_c"], hour["dewpoint_f"], hour["will_it_rain"],
                    hour["chance_of_rain"], hour["will_it_snow"], hour["chance_of_snow"],
                    hour["vis_km"], hour["vis_miles"], hour["gust_mph"], hour["gust_kph"],
                    hour["uv"], hour.get("short_rad", ""), hour.get("diff_rad", "")
                ])

    print(f"Data successfully written to {file_path}")

if __name__ == "__main__":
    location = "Freiburg"
    file_path = "../data/weatherdata/weather_data.csv"


    weather_data = fetch_weather_data(location)
    if weather_data:
        save_weather_data_to_csv(weather_data, file_path)
