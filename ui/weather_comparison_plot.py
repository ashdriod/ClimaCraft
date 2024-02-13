import csv
import subprocess
import os

def generate_weather_comparison_graph(csv_file_path, output_file_path):
    # Read the CSV file and extract the data
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Skip the header
        actual_data = next(reader)
        predicted_data = next(reader)

    # GNUPlot command file content, adjusted for the given CSV structure
    gnuplot_commands = f"""
    set terminal pngcairo size 800,600
    set output '{output_file_path}'
    set style data histograms
    set style histogram cluster gap 1
    set style fill solid border -1
    set boxwidth 0.9
    set grid ytics
    set xtics rotate by -45
    set title "Actual vs Predicted Weather Conditions"
    set ylabel "Values"
    set key outside
    set auto x
    set yrange [0:*]

    # Plotting the data
    plot '-' using 2:xtic(1) title 'Actual', '-' using 2:xtic(1) title 'Predicted'
    """

    # Append actual data to GNUPlot commands
    for i, header in enumerate(headers):
        gnuplot_commands += f"'{header}' {actual_data[i]}\n"
    gnuplot_commands += "e\n"  # End of actual data

    # Append predicted data to GNUPlot commands
    for i, header in enumerate(headers):
        gnuplot_commands += f"'{header}' {predicted_data[i]}\n"
    gnuplot_commands += "e\n"  # End of predicted data

    # Write GNUPlot command to a temporary file
    gnuplot_script_path = '/tmp/tmp_gnuplot_script.gp'
    with open(gnuplot_script_path, 'w') as file:
        file.write(gnuplot_commands)

    # Call GNUPlot with the command file
    subprocess.run(['gnuplot', gnuplot_script_path])

    # Optionally, you can delete the temporary script file after execution
    os.remove(gnuplot_script_path)

    print(f"Bar graph generated and saved to {output_file_path}")

