import os
import gi# Import the pango module
from gi.overrides import GdkPixbuf
import threading
from gi.repository import GLib
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from api.weather import get_simplified_weather_info
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
        # Simulate a button click
        self.simulate_button_click()

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_file_path = "css/style.css"

        # Load the CSS file
        css_provider.load_from_path(css_file_path)

        # Apply the CSS to the application
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Assuming 'main_window' is the ID for your main window in the Glade file
        window = self.builder.get_object("main_window")
        window.get_style_context().add_class("window")

    def on_button_clicked(self, widget):
        # Get the TextView object instead of the label
        weather_text_view = self.builder.get_object("weather_text_view")
        weather_info = get_simplified_weather_info()  # Use the simplified function

        # GtkTextView uses a GtkTextBuffer for its text content
        text_buffer = weather_text_view.get_buffer()

        # Use GLib.idle_add to update the UI from within a thread
        GLib.idle_add(text_buffer.set_text, weather_info)

        # Start the background task
        threading.Thread(target=self.background_task, args=(weather_text_view,)).start()



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

    def simulate_button_click(self):
        # Assuming the button's ID is "my_button" in your Glade file
        button = self.builder.get_object("my_button")
        self.on_button_clicked(button)  # Directly call the event handler

        # Alternatively, if you want to simulate a 'clicked' signal
        # button.emit("clicked")
if __name__ == "__main__":
    app = MyWindow()
    Gtk.main()
