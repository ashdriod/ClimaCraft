import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk  # Updated to include Gdk for CSS styling

# Import the get_weather function from the weather module
from api.weather import get_weather


class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Weather App")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # Apply CSS to the window
        self.apply_css()

        self.button = Gtk.Button(label="Get Weather")
        self.button.connect("clicked", self.on_button_clicked)
        self.label = Gtk.Label(label="Press the button to get the weather.")

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.box.pack_start(self.button, True, True, 0)
        self.box.pack_start(self.label, True, True, 0)

    def apply_css(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path('css/style.css')
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_button_clicked(self, widget):
        # Use the get_weather function to set the label text
        weather_info = get_weather()
        self.label.set_text(weather_info)


