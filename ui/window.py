import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk
from api.weather import get_weather

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
        # Use the get_weather function to set the label text
        weather_label = self.builder.get_object("weather_label")
        weather_info = get_weather()
        weather_label.set_text(weather_info)

    def on_main_window_destroy(self, widget):
        Gtk.main_quit()

if __name__ == "__main__":
    app = MyWindow()
    Gtk.main()
