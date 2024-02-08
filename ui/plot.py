import os
import subprocess

def generate_gnuplot_image(image_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    # Prepare the GNUplot script
    script_content = f"""
    set terminal pngcairo enhanced
    set output '{image_path}'
    set title "Weather Data"
    set xlabel "Sample"
    set ylabel "Value"
    plot sin(x) with lines title 'Sample Data'
    """

    # Write the script to a temporary file
    temp_script_path = "temp_gnuplot_script.gp"
    with open(temp_script_path, "w") as script_file:
        script_file.write(script_content)

    # Execute the GNUplot script
    subprocess.run(["gnuplot", temp_script_path])

    # Remove the temporary script file after execution
    os.remove(temp_script_path)
