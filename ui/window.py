import os
import shutil
import subprocess

import gi
from gi.overrides import GdkPixbuf
import threading
from gi.repository import GLib

from ui.weatherlatex import get_weather_data_as_latex

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from api.weather import get_simplified_weather_info, get_wind_and_pressure_info, get_additional_weather_info, get_weather
from .temp_plot import generate_dual_axis_graph
from .daily_overview import generate_temperature_overview_graph
from api.forecast import fetch_weather_data, save_weather_data_to_csv
from .windtemp import generate_wind_temperature_graph


class MyWindow:
    def __init__(self):
        # Initialize the window by loading the UI from a Glade file and setting up the environment.
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window.glade")
        self.builder.connect_signals(self)

        self.apply_css()

        # Retrieve the main window widget and display it.
        self.window = self.builder.get_object("main_window")
        self.window.set_default_size(400, 200)
        self.window.show_all()

        self.simulate_button_click()

        # Configure CSS identifiers for specific widgets.
        wind_pressure_text_view = self.builder.get_object("wind_and_pressure_info")
        if wind_pressure_text_view:
            wind_pressure_text_view.set_name("wind_and_pressure_info_view")

        additional_weather_label = self.builder.get_object("additional_weather_info")
        if additional_weather_label:
            additional_weather_label.set_name("additional_weather_info_view")

    def apply_css(self):
        # Apply custom CSS to the application.
        css_provider = Gtk.CssProvider()
        css_file_path = "css/style.css"
        css_provider.load_from_path(css_file_path)

        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        window = self.builder.get_object("main_window")
        window.get_style_context().add_class("window")

    def on_button_clicked(self, widget):
        # Retrieve weather information and update the TextView and Label widgets
        weather_text_view = self.builder.get_object("weather_text_view")
        weather_info = get_simplified_weather_info()
        wind_and_pressure_info = get_wind_and_pressure_info()
        additional_weather_info = get_additional_weather_info()

        # Update the main weather information display
        if weather_text_view:
            text_buffer = weather_text_view.get_buffer()
            GLib.idle_add(text_buffer.set_text, weather_info)

        # Update the additional weather information display
        additional_weather_label = self.builder.get_object("additional_weather_info")
        if additional_weather_label:
            GLib.idle_add(additional_weather_label.set_text, additional_weather_info)

        # Update the wind and pressure information display
        wind_pressure_text_view = self.builder.get_object("wind_and_pressure_info")
        if wind_pressure_text_view:
            formatted_info = "\n Wind and Pressure Information\n\n\n" + wind_and_pressure_info
            wind_pressure_text_buffer = wind_pressure_text_view.get_buffer()
            GLib.idle_add(wind_pressure_text_buffer.set_text, formatted_info)

        # Initiate background task for additional weather data processing
        threading.Thread(target=self.background_task, args=(weather_text_view,)).start()

    def on_download_latex_clicked(self, widget):
        location = "Freiburg"  # Or get this dynamically from your GUI
        latex_content = get_weather_data_as_latex(location)

        latex_file_path = "latex/weather_report.tex"
        output_directory = "latex"  # Specify the output directory

        # Ensure the output directory exists
        os.makedirs(output_directory, exist_ok=True)

        # Write the LaTeX content to a file directly
        with open(latex_file_path, "w") as file:
            file.write(latex_content)  # Write the complete latex_content as it is

        # Command to compile the LaTeX file to PDF and specify the output directory
        compile_command = [
            "pdflatex",
            "-interaction=nonstopmode",
            f"-output-directory={output_directory}",
            latex_file_path
        ]

        try:
            # Run the command
            result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
                                    text=True)
            # Check for success
            if result.returncode == 0:
                print(f"Compilation successful. PDF saved in '{output_directory}' directory.")
            else:
                print("LaTeX compilation failed:", result.stderr)
        except subprocess.CalledProcessError as e:
            print("Error during compilation:", e)

    def background_task(self, weather_label):
        # Fetch and process weather data, then update the GUI with graphs
        location = "Freiburg"
        weather_data = fetch_weather_data(location)
        if weather_data:
            file_path = "data/weatherdata/weather_data.csv"
            save_weather_data_to_csv(weather_data, file_path)

            # Generate and display various weather-related graphs
            temp_precip_image_path = "data/graph/temperature_precipitation_graph.png"
            generate_dual_axis_graph(file_path, temp_precip_image_path)
            GLib.idle_add(self.display_plot_image, temp_precip_image_path, "plot_image")

            wind_temp_image_path = "data/graph/wind_temperature_graph.png"
            generate_wind_temperature_graph(file_path, wind_temp_image_path)
            GLib.idle_add(self.display_plot_image, wind_temp_image_path, "plot_image2")

            daily_overview_image_path = "data/graph/temperature_overview.png"
            generate_temperature_overview_graph(file_path, daily_overview_image_path)
            GLib.idle_add(self.display_plot_image, daily_overview_image_path, "plot_image3")

    def display_plot_image(self, image_path, image_widget_name):
        # Display a plot image in the specified widget
        if os.path.exists(image_path):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 600, 550, True)
            plot_image_widget = self.builder.get_object(image_widget_name)
            plot_image_widget.set_from_pixbuf(pixbuf)
        else:
            print(f"Error: The image file {image_path} does not exist.")

    def on_main_window_destroy(self, widget):
        # Terminate the application
        Gtk.main_quit()

    def simulate_button_click(self):
        # Simulate a button click for testing purposes
        button = self.builder.get_object("my_button")
        self.on_button_clicked(button)

if __name__ == "__main__":
    app = MyWindow()
    Gtk.main()

