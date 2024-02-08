import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Adjust the import path if necessary based on your project structure
from ui.window import MyWindow

def main():
    # The MyWindow class now handles everything, including showing the window and connecting the destroy signal
    MyWindow()
    Gtk.main()

if __name__ == "__main__":
    main()
