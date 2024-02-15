import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# The MyWindow class now handles everything, including showing the window and connecting the destroy signal
from ui.window import MyWindow

def main():
    # Create an instance of the MyWindow class and start the GTK main loop
    MyWindow()
    Gtk.main()

if __name__ == "__main__":
    main()
