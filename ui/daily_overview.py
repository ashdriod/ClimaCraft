import os
import subprocess
import csv
from datetime import datetime, timedelta
from collections import defaultdict

def preprocess_temperature_data(csv_file_path, output_csv_path):
    """Preprocess the data to get daily max, min, and average temperatures."""
    temp_data = defaultdict(list)

    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = datetime.strptime(row['Time'], '%Y-%m-%d %H:%M').date()
            temp_c = float(row['Temperature (C)'])
            temp_data[date].append(temp_c)

    with open(output_csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Date', 'Max Temp (C)', 'Min Temp (C)', 'Avg Temp (C)'])
        for date, temps in temp_data.items():
            max_temp = max(temps)
            min_temp = min(temps)
            avg_temp = sum(temps) / len(temps)
            writer.writerow([date, max_temp, min_temp, avg_temp])

def generate_temperature_overview_graph(input_csv_path, image_path):
    """Generate a graph showing max, min, and average temperature."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    script_content = f"""
    set terminal pngcairo transparent enhanced size 800,600
    set output '{image_path}'
    set datafile separator comma
    set key outside
    set grid
    set title "Daily Temperature Overview"
    set xlabel "Date"
    set ylabel "Temperature (°C)"
    set xdata time
    set timefmt "%Y-%m-%d"
    set format x "%d-%m"
    set autoscale xfix
    set style line 1 lc rgb 'red' lt 1 lw 2 pt 7 ps 1.5   # Max Temp
    set style line 2 lc rgb 'blue' lt 1 lw 2 pt 7 ps 1.5 # Min Temp
    set style line 3 lc rgb 'green' lt 1 lw 2 pt 7 ps 1.5 # Avg Temp
    plot \\
    '{input_csv_path}' using 1:2 with linespoints linestyle 1 title 'Max Temp (C)', \\
    '{input_csv_path}' using 1:3 with linespoints linestyle 2 title 'Min Temp (C)', \\
    '{input_csv_path}' using 1:4 with linespoints linestyle 3 title 'Avg Temp (C)'
    """

    temp_script_path = "temp_gnuplot_script.gp"
    with open(temp_script_path, "w") as script_file:
        script_file.write(script_content)

    # Execute the GNUplot script
    subprocess.run(["gnuplot", temp_script_path])

    # Clean up: remove the temp script file
    os.remove(temp_script_path)
    print(f"Graph generated and saved to {image_path}")

# Path to your CSV data
csv_file_path = "data/weatherdata/weather_data.csv"
output_csv_path = "data/weatherdata/processed_temp_data.csv"

# Preprocess the data to get the required format
preprocess_temperature_data(csv_file_path, output_csv_path)

# Generate the temperature overview graph
image_path = "data/graph/temperature_overview.png"
generate_temperature_overview_graph(output_csv_path, image_path)
