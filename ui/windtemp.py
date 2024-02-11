import os
import subprocess
import csv
from datetime import datetime

def get_months_from_csv(csv_file_path):
    months = set()
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            if row:  # Check if row is not empty
                date_str = row[0]  # Assuming the first column is the date in 'YYYY-MM-DD HH:MM' format
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                months.add(date_obj.strftime("%B"))  # Extract the month name and add to the set
    return sorted(list(months))  # Return a sorted list of unique month names

def generate_wind_temperature_graph(csv_file_path, image_path, desired_width=600, desired_height=550):
    months = get_months_from_csv(csv_file_path)
    month_label = " and ".join(months)  # Join month names with 'and' if there are two, otherwise just one name

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    script_content = f"""
    set terminal pngcairo size {desired_width},{desired_height} transparent enhanced
    set output '{image_path}'
    set datafile separator comma
    set xdata time
    set timefmt "%Y-%m-%d %H:%M"
    set format x "%d"  # Display only the day
    set xlabel "Day of {month_label}"
    set ylabel "Temperature (°C)"
    set y2label "Wind Speed (KPH)"
    set ytics nomirror
    set y2tics
    set grid
    set title "Wind Speed and Direction with Temperature Over Time for {month_label}"
    set style line 1 lt 1 lw 2 lc rgb "red"  # Line style for temperature
    set style line 2 lt 2 lw 2 lc rgb "blue"  # Line style for wind vectors
    plot \\
    "{csv_file_path}" using 1:2 with lines linestyle 1 title "Temperature", \\
    "{csv_file_path}" using 1:9:($9*cos($11)):($9*sin($11)) with vectors filled head lc 'blue' title 'Wind Vectors'
    """.format(image_path=image_path, csv_file_path=csv_file_path, month_label=month_label)

    temp_script_path = "temp_gnuplot_script.gp"
    with open(temp_script_path, "w") as script_file:
        script_file.write(script_content)

    subprocess.run(["gnuplot", temp_script_path])
    os.remove(temp_script_path)
    print(f"Graph generated and saved to {image_path}")

    # Additional code for wind direction vectors
    additional_script_content = """
    set terminal pngcairo size 800,600 enhanced
    set output 'wind_direction_vectors.png'
    set datafile separator comma
    set xdata time
    set timefmt "%Y-%m-%d %H:%M"
    set format x "%d-%m"  # Customize based on your CSV's date format
    set xlabel "Time"
    set ylabel "Wind Speed (KPH)"
    set yrange [0:]  # Adjust based on your data
    set grid
    set title "Wind Direction and Speed Vectors"

    # Convert wind direction from degrees to radians for trigonometric calculations
    wind_dir_to_radians(deg) = deg * pi / 180

    # Assuming 'I' is wind speed and 'K' is wind direction
    plot '{csv_file_path}' using 1:($0):($8*cos(wind_dir_to_radians($10))):($8*sin(wind_dir_to_radians($10))) with vectors filled head lc 'blue' title 'Wind Vectors'
    """
    additional_script_path = "additional_gnuplot_script.gp"
    with open(additional_script_path, "w") as additional_script_file:
        additional_script_file.write(additional_script_content)

    subprocess.run(["gnuplot", additional_script_path])
    os.remove(additional_script_path)
    print("Additional graph generated and saved to wind_direction_vectors.png")

# Example usage
csv_file_path = "data/weatherdata/weather_data.csv"
image_path = "data/graph/wind_temperature_graph.png"
generate_wind_temperature_graph(csv_file_path, image_path)
