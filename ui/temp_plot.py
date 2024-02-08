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
                date_str = row[0]  # Assuming the first column is the date
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                months.add(date_obj.strftime("%B"))  # Extract the month name
    return " and ".join(sorted(list(months)))  # Join month names with 'and'

def generate_dual_axis_graph(csv_file_path, image_path, desired_width=1280, desired_height=720):
    months_label = get_months_from_csv(csv_file_path)
    month_or_months = "Month" if " and " not in months_label else "Months"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    # Adjust the GNUplot script for readability and transparency
    script_content = f"""
    set terminal pngcairo transparent enhanced size {desired_width},{desired_height}
    set output '{image_path}'
    set datafile separator comma
    set xdata time
    set timefmt "%Y-%m-%d %H:%M"
    set format x "%d"  # Display only the day of the month
    set xlabel "{month_or_months}: {months_label}"
    set ylabel "Temperature (°C)"
    set y2label "Chance of Rain (%)"
    set ytics nomirror
    set y2tics
    set grid
    set title "Temperature and Precipitation Chance Over Time ({months_label})"
    set style line 1 lt 1 lw 2 lc rgb "red"  # Thicker line for temperature
    set style line 2 lt 2 lw 2 lc rgb "blue"  # Thicker line for precipitation chance
    plot \\
    "{csv_file_path}" using 1:2 with lines linestyle 1 title "Temperature", \\
    "{csv_file_path}" using 1:3 axes x1y2 with lines linestyle 2 title "Chance of Rain"
    """.format(image_path=image_path, csv_file_path=csv_file_path, months_label=months_label, month_or_months=month_or_months)

    # Temp file to hold the GNUplot script
    temp_script_path = "temp_gnuplot_script.gp"
    with open(temp_script_path, "w") as script_file:
        script_file.write(script_content)

    # Execute the GNUplot script
    subprocess.run(["gnuplot", temp_script_path])

    # Clean up: remove the temp script file
    os.remove(temp_script_path)
    print(f"Graph generated and saved to {image_path}")

# Example usage
csv_file_path = "data/weatherdata/weather_data.csv"
image_path = "data/graph/dual_axis_graph.png"
generate_dual_axis_graph(csv_file_path, image_path)
