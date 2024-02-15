import csv
import os
import subprocess
from datetime import datetime


# Function to extract unique month names from a CSV file based on dates in the first column.
def get_months_from_csv(csv_file_path):
    months = set()
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header to process only data rows.
        for row in reader:
            if row:  # Ensure the row is not empty.
                date_str = row[0]  # Date is expected in the first column.
                date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M")  # Parse date.
                months.add(date_obj.strftime("%B"))  # Add the month name to a set for uniqueness.
    return sorted(list(months))  # Return a list of sorted month names.


# Function to generate a graph for wind speed, gust, and direction from a CSV file.
def wind_speed_gust_direction(csv_file_path, image_path, desired_width=800, desired_height=600):
    months = get_months_from_csv(csv_file_path)  # Extract month names for labeling.
    month_label = " and ".join(months)  # Format month names into a string.

    os.makedirs(os.path.dirname(image_path), exist_ok=True)  # Ensure output directory exists.

    # Prepare GNUplot script for generating the graph.
    script_content = f"""
    set terminal pngcairo size {desired_width},{desired_height} transparent enhanced
    set output '{image_path}'
    set datafile separator comma
    set xdata time
    set timefmt "%Y-%m-%d %H:%M"
    set format x "%d"  # Show day of the month on the x-axis.
    set xlabel "Day of {month_label}"
    set ylabel "Wind Speed and Gust (KPH)"
    set y2label "Wind Direction (Degrees)"
    set ytics nomirror
    set y2tics 0, 90, 360
    set grid
    set title "Wind Speed, Gust, and Direction Over Time for {month_label}"
    set style line 1 lt 1 lw 2 lc rgb "blue"  # Style for wind speed.
    set style line 2 lt 2 lw 2 lc rgb "green"  # Style for gust.
    set style line 3 lt 3 lw 2 lc rgb "red"  # Style for wind direction.
    plot \\
    "{csv_file_path}" using 1:9 with lines linestyle 1 title "Wind Speed (KPH)", \\
    "{csv_file_path}" using 1:33 with lines linestyle 2 title "Gust (KPH)", \\
    "{csv_file_path}" using 1:10 axes x1y2 with lines linestyle 3 title "Wind Direction"
    """.format(image_path=image_path, csv_file_path=csv_file_path,
               month_label=month_label)  # Dynamically insert variables into the script.

    temp_script_path = "temp_gnuplot_script.gp"  # Temporary file for the script.
    with open(temp_script_path, "w") as script_file:
        script_file.write(script_content)  # Write the script content to the file.

    subprocess.run(["gnuplot", temp_script_path])  # Execute the GNUplot script.
    os.remove(temp_script_path)  # Delete the temporary script file after use.
    print(f"Graph generated and saved to {image_path}")  # Notify the user of successful graph generation.
