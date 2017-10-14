import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib, Gdk

from DrawingArea import DrawingArea, Grid
from controller import *


class AppWin(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.connect("button-press-event", self.on_button_press)
        self.connect("key-press-event", self.on_key_press)

        self.resize(500, 500)
        self.set_position(Gtk.WindowPosition.CENTER)

        self.area = DrawingArea(500, 500)
        wGrid = Grid(400, 400, 9, 9)
        wGrid.set_cell_color(4, 4, (50, 180, 220))

        self.controller = Controller(wGrid)
        self.change_sudoku('Sudoku 1')

        sugestionGrid = Grid(60, 60, 3, 3, 1, False)
        sugestionGrid.set_position(9 * wGrid.cell_size + 5, 0)
        self.sugest_controller = SugestionController(
            sugestionGrid, self.controller)

        self.area.add_widget(wGrid)
        self.area.add_widget(Grid(400, 400, 3, 3, 4, False))
        #g = Grid(400, 400, 27, 27, 1, False)
        #g.set_position(3,3)
        #self.area.add_widget(g)
        self.area.add_widget(sugestionGrid)

        self.add(self.area)

        self.show_all()

    def change_sudoku(self, name):
        file_name = 'games/s1.txt'
        if name == 'Sudoku 2':
            file_name = 'games/s2.txt'

        sudoku = SudokuFile(file_name).read()
        self.controller.set_sudoku(sudoku)
        self.area.queue_draw()

    def on_button_press(self, w, e):
        self.controller.mouse_event(e)
        self.sugest_controller.mouse_event(e)
        self.area.queue_draw()

    def on_key_press(self, w, e):
        self.controller.keyboard_event(e)
        self.sugest_controller.keyboard_event(e)
        self.area.queue_draw()


class App(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="sudoku.gtk", **kwargs)

        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new('about', None)
        action.connect('activate', self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new('quit', None)
        action.connect('activate', self.on_quit)
        self.add_action(action)

        builder = Gtk.Builder.new_from_file("menu.ui")
        self.set_app_menu(builder.get_object('app-menu'))

        sud_variant = GLib.Variant.new_string("Sudoku 1")
        sud_action = Gio.SimpleAction.new_stateful("change_sudoku", sud_variant.get_type(),
                                               sud_variant)
        sud_action.connect("change-state", self.on_change_sudoku_state)
        self.add_action(sud_action)

    def on_change_sudoku_state(self, action, value):
        if action.get_state() != value:
            action.set_state(value)
            self.window.change_sudoku(value.get_string())

    def do_activate(self):
        if not self.window:
            self.window = AppWin(application=self, title="Sudoku")

        self.window.present()

    def on_about(self, action, param):
        about_dialog = Gtk.AboutDialog(transient_for=self.window, modal=True)
        about_dialog.set_program_name('Sudoku')
        about_dialog.set_license('LICENSE_UNKNOWN')
        about_dialog.set_website_label('GitHub')
        about_dialog.set_website('https://github.com/Felipe-Aquino/sudoku-gtk')
        about_dialog.set_authors(['Felipe'])
        about_dialog.present()

    def on_quit(self, action, param):
        self.quit()


if __name__ == "__main__":
    app = App()
    app.run(sys.argv)
