# main.py
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Import the get_weather function from the weather module
from api.weather import get_weather

class MyWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Weather App")

        self.button = Gtk.Button(label="Get Weather")
        self.button.connect("clicked", self.on_button_clicked)
        self.label = Gtk.Label()

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(self.box)

        self.box.pack_start(self.button, False, False, 0)
        self.box.pack_start(self.label, False, False, 0)

    def on_button_clicked(self, widget):
        # Use the get_weather function to set the label text
        weather_info = get_weather()
        self.label.set_text(weather_info)

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
