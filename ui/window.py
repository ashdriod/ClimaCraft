import os

import gi
from gi.overrides import GdkPixbuf

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from api.weather import get_weather
from .plot import generate_gnuplot_image
from api.forecast import fetch_weather_data, save_weather_data_to_csv


class MyWindow:
    def __init__(self):
        # Load UI from Glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file("ui/window.glade")
        self.builder.connect_signals(self)

        # Apply CSS
        self.apply_css()

        # Get the main window and show it
        self.window = self.builder.get_object("main_window")
        self.window.set_default_size(400, 200)
        self.window.show_all()


    def apply_css(self):
        css = b"""
        .window {
            background: linear-gradient(to right, #3498db, #88c3ff);
        }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        window = self.builder.get_object("main_window")
        window.get_style_context().add_class("window")

    def on_button_clicked(self, widget):
        # Assuming get_weather() is correctly fetching a summary string for display
        weather_label = self.builder.get_object("weather_label")
        weather_info = get_weather()  # Update this call as needed
        weather_label.set_text(weather_info)

        # Fetch detailed weather data and save it to CSV
        location = "Freiburg"  # Or dynamically set based on user input or other logic
        weather_data = fetch_weather_data(location)
        if weather_data:
            file_path = "data/weatherdata/weather_data.csv"  # Ensure this path exists
            save_weather_data_to_csv(weather_data, file_path)
            print(f"Weather data for {location} saved to {file_path}")

        # Optional: Generate and display a plot based on the newly saved CSV
        plot_image_path = "data/graph/test_plot.png"
        # You would need to implement generate_gnuplot_image to create a plot from the CSV
        generate_gnuplot_image(plot_image_path)  # Adjust this function as needed
        # Load and display the generated image in the GtkImage widget
        self.display_plot_image(plot_image_path)

    def display_plot_image(self, image_path):
        # Check if the image file exists
        if os.path.exists(image_path):
            # Load the image from the file
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
            plot_image_widget = self.builder.get_object("plot_image")
            plot_image_widget.set_from_pixbuf(pixbuf)
        else:
            print(f"Error: The image file {image_path} does not exist.")

    def on_main_window_destroy(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    app = MyWindow()
    Gtk.main()
