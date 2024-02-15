import csv
import os
import subprocess


def generate_weather_comparison_graph(csv_file_path, output_file_path):
    # Open and read CSV file to extract actual and predicted weather data
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip the header row to get data categories
        actual_data = next(reader)  # First data row for actual weather conditions
        predicted_data = next(reader)  # Second data row for predicted weather conditions

    # Prepare GNUPlot commands to generate a comparison graph
    gnuplot_commands = f"""
    set terminal pngcairo transparent size 800,600 enhanced font 'Verdana,10'  # Graph settings
    set output '{output_file_path}'  # Output file path
    set style data histograms  # Histogram plot style
    set style histogram cluster gap 1  # Histogram appearance
    set style fill solid border -1  # Fill style
    set boxwidth 0.9  # Width of the histogram bars
    set grid ytics  # Y-axis grid
    set xtics rotate by -45  # X-axis labels rotated for readability
    set title "Actual vs Predicted Weather Conditions"  # Graph title
    set ylabel "Values"  # Y-axis label
    set key outside  # Legend placement
    set auto x  # Auto-set x-axis
    set yrange [0:*]  # Y-axis range
    plot '-' using 2:xtic(1) title 'Actual', '-' using 2:xtic(1) title 'Predicted'  # Plotting data
    """

    # Append actual weather data to the GNUPlot commands
    for i, header in enumerate(headers):
        gnuplot_commands += f"'{header}' {actual_data[i]}\n"
    gnuplot_commands += "e\n"  # End of actual data section

    # Append predicted weather data to the GNUPlot commands
    for i, header in enumerate(headers):
        gnuplot_commands += f"'{header}' {predicted_data[i]}\n"
    gnuplot_commands += "e\n"  # End of predicted data section

    # Write GNUPlot commands to a temporary script file
    gnuplot_script_path = '/tmp/tmp_gnuplot_script.gp'
    with open(gnuplot_script_path, 'w') as file:
        file.write(gnuplot_commands)

    # Execute GNUPlot with the generated script file to create the graph
    subprocess.run(['gnuplot', gnuplot_script_path])

    # Clean up by deleting the temporary GNUPlot script file
    os.remove(gnuplot_script_path)

    # Notify the user of successful graph generation
    print(f"Bar graph generated and saved to {output_file_path}")
