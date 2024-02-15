import csv
import os
import subprocess
from datetime import datetime


# Function to extract unique months from a CSV file
def get_months_from_csv(csv_file_path):
    months = set()
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row.
        for i, row in enumerate(reader):
            # Consider every 24th record (hourly data) to represent a day.
            if i % 24 == 0 and row:
                date_str = row[0]
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                months.add(date_obj.strftime("%B"))
            if i >= 24 * 5:  # Stop after 6 days of data.
                break
    return " and ".join(sorted(list(months)))  # Format month names.


# Function to generate a dual-axis graph for temperature and precipitation from a CSV file.
def generate_dual_axis_graph(csv_file_path, image_path, desired_width=1280, desired_height=720):
    months_label = get_months_from_csv(csv_file_path)
    month_or_months = "Month" if " and " not in months_label else "Months"

    # Create the output directory if it doesn't exist.
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    # GNUplot script for generating a dual-axis graph.
    script_content = f"""
    set terminal pngcairo transparent enhanced size {desired_width},{desired_height}
    set output '{image_path}'
    set datafile separator comma
    set xdata time
    set timefmt "%Y-%m-%d %H:%M"
    set format x "%d"  # Show day of the month on the x-axis.
    set xlabel "{month_or_months}: {months_label}"
    set ylabel "Temperature (°C)"
    set y2label "Precipitation (mm)"
    set ytics nomirror
    set y2tics
    set y2range [0:*]  # Auto-adjust the precipitation range.
    set grid
    set title "Temperature and Precipitation Over Time ({months_label})"
    set style line 1 lt 1 lw 2 lc rgb "red"  # Style for temperature.
    set style line 2 lt 2 lw 2 lc rgb "blue"  # Style for precipitation.
    plot \\
    "{csv_file_path}" using 1:2 with lines linestyle 1 title "Temperature", \\
    "{csv_file_path}" using 1:14 axes x1y2 with lines linestyle 2 title "Precipitation"
    """.strip()

    # Create a temporary file for the GNUplot script.
    temp_script_path = "temp_gnuplot_script.gp"
    with open(temp_script_path, "w") as script_file:
        script_file.write(script_content)

    # Execute the GNUplot script to generate the graph.
    subprocess.run(["gnuplot", temp_script_path])

    # Remove the temporary script file after use.
    os.remove(temp_script_path)
    print(f"Graph generated and saved to {image_path}")
