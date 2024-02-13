import csv

def create_weather_comparison_csv():
    # Read the current weather data from Freiburg weather data file
    with open('data/weatherdata/freiburg_weather_data.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        freiburg_weather = next(reader)  # Read the first line of actual data

    # Calculate the index for the predicted weather data
    hour = int(freiburg_weather[0])  # Now correctly reading the 'HH' format
    predicted_row_index = hour + 2  # Adjusting to get the 16th row as an example

    # Read the predicted weather data from the general weather data file
    with open('data/weatherdata/weather_data.csv', mode='r') as file:
        reader = list(csv.reader(file))
        predicted_weather = reader[predicted_row_index + 1]  # Skip header manually by adjusting index

    # Prepare the data for the new CSV file
    new_row_1 = [
        freiburg_weather[2],  # temperature_c
        freiburg_weather[4],  # wind_kph
        str(float(freiburg_weather[6]) / 100),  # pressure_mb, adjusted
        str(float(freiburg_weather[7]) / 10),  # humidity, adjusted
        freiburg_weather[10]  # visibility_km
    ]

    new_row_2 = [
        predicted_weather[1],  # temperature_c
        predicted_weather[8],  # wind_kph
        str(float(predicted_weather[11]) / 100),  # pressure_mb, adjusted
        str(float(predicted_weather[16]) / 10),  # humidity, adjusted
        predicted_weather[30]  # visibility_km
    ]

    # Write the new data to a CSV file in the specified directory
    with open('data/weatherdata/new_weather_comparison.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Temperature_C', 'Wind_KPH', 'Pressure_MB', 'Humidity', 'Visibility_KM'])
        writer.writerow(new_row_1)
        writer.writerow(new_row_2)

