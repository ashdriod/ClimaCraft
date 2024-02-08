import os

import gi
from gi.overrides import GdkPixbuf
import threading
from gi.repository import GLib
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from api.weather import get_weather
from .temp_plot import generate_dual_axis_graph
from .daily_overview import generate_temperature_overview_graph
from api.forecast import fetch_weather_data, save_weather_data_to_csv
from .windtemp import generate_wind_temperature_graph



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
        # Immediately update the label with current weather info
        weather_label = self.builder.get_object("weather_label")
        weather_info = get_weather()  # Assuming this returns a string of weather info
        GLib.idle_add(weather_label.set_text, weather_info)

        # Start the background task
        threading.Thread(target=self.background_task, args=(weather_label,)).start()

    from gi.repository import GdkPixbuf, GLib

    def background_task(self, weather_label):
        location = "Freiburg"
        weather_data = fetch_weather_data(location)
        if weather_data:
            file_path = "data/weatherdata/weather_data.csv"
            save_weather_data_to_csv(weather_data, file_path)
            print(f"Weather data for {location} saved to {file_path}")

            # Temperature and Precipitation Graph
            temp_precip_image_path = "data/graph/temperature_precipitation_graph.png"
            generate_dual_axis_graph(file_path, temp_precip_image_path)
            GLib.idle_add(self.display_plot_image, temp_precip_image_path, "plot_image")

            # Wind Speed and Direction with Temperature Graph
            wind_temp_image_path = "data/graph/wind_temperature_graph.png"
            generate_wind_temperature_graph(file_path, wind_temp_image_path)
            GLib.idle_add(self.display_plot_image, wind_temp_image_path, "plot_image2")

            # Comparative Daily Overview Graph
            daily_overview_image_path = "data/graph/temperature_overview.png"
            generate_temperature_overview_graph(file_path, daily_overview_image_path)  # Assume this function is defined
            GLib.idle_add(self.display_plot_image, daily_overview_image_path, "plot_image3")

    def display_plot_image(self, image_path, image_widget_name):
        if os.path.exists(image_path):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(image_path, 600, 550,
                                                             True)  # Adjust these dimensions as needed
            plot_image_widget = self.builder.get_object(image_widget_name)
            plot_image_widget.set_from_pixbuf(pixbuf)
        else:
            print(f"Error: The image file {image_path} does not exist.")

    def on_main_window_destroy(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    app = MyWindow()
    Gtk.main()
