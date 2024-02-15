import csv


def create_weather_comparison_csv():
    # Open and read actual weather data from Freiburg.
    with open('data/weatherdata/freiburg_weather_data.csv', mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header.
        freiburg_weather = next(reader)  # Get actual weather data.

    # Calculate index for predicted weather data based on the hour.
    hour = int(freiburg_weather[0])  # Extract hour from Freiburg data.
    predicted_row_index = hour  # Determine index for predicted data.

    # Open and read predicted weather data.
    with open('data/weatherdata/weather_data.csv', mode='r') as file:
        reader = list(csv.reader(file))
        predicted_weather = reader[predicted_row_index + 1]  # Get predicted weather data.

    # Prepare data for comparison CSV.
    new_row_1 = [
        freiburg_weather[2],  # Temperature from Freiburg data.
        freiburg_weather[4],  # Wind speed from Freiburg data.
        str(float(freiburg_weather[6]) / 100),  # Pressure, adjusted from Freiburg data.
        str(float(freiburg_weather[7]) / 10),  # Humidity, adjusted from Freiburg data.
        freiburg_weather[10]  # Visibility from Freiburg data.
    ]

    new_row_2 = [
        predicted_weather[1],  # Temperature from predicted data.
        predicted_weather[8],  # Wind speed from predicted data.
        str(float(predicted_weather[11]) / 100),  # Pressure, adjusted from predicted data.
        str(float(predicted_weather[16]) / 10),  # Humidity, adjusted from predicted data.
        predicted_weather[30]  # Visibility from predicted data.
    ]

    # Write the actual and predicted weather data to a new CSV file.
    with open('data/weatherdata/current_vs_forcasted_weather.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Temperature_C', 'Wind_KPH', 'Pressure_MB', 'Humidity', 'Visibility_KM'])  # Column headers.
        writer.writerow(new_row_1)  # Actual weather data row.
        writer.writerow(new_row_2)  # Predicted weather data row.
