import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# Adjust the import path if necessary based on your project structure
from ui.window import MyWindow

def main():
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
