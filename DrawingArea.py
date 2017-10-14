import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from Color import Color


class DrawWidget:
    def draw(self, cairo): pass

    def update(self): pass


class Cell:
    def __init__(self, x, y, size, color=Color.WHITE, text='', text_color=Color.BLACK):
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.text_color = text_color
        self.size = size
        self.row = y // size
        self.col = x // size

    def is_inside(self, x, y):
        return self.x <= x and x <= self.x + self.size and self.y <= y and y <= self.y + self.size

    def show_text(self, cr):
        _, _, width, height, dx, _ = cr.text_extents(self.text)

        cx = self.x + self.size / 2
        cy = self.y + self.size / 2

        cr.move_to(cx - dx / 2, cy + height / 2)

        cr.set_source_rgb(*self.text_color)
        cr.show_text(self.text)


class Grid(DrawWidget):
    def __init__(self, width, height, rows=1, cols=1, stroke=2, fill=True, text_color=Color.BLACK):
        self.rows = rows if rows > 0 else 1
        self.cols = cols if cols > 0 else 1
        self.stroke = stroke
        self.fill = fill

        scale = min(width, height) / 300.0
        self.cell_size = int(200 * scale / ((3 / 4.0) * self.rows))
        self.position = 0, 0

        self.cells = []
        for y in range(0, self.cell_size * self.cols, self.cell_size):
            row = []
            for x in range(0, self.cell_size * self.rows, self.cell_size):
                row.append(Cell(x, y, self.cell_size, text_color=text_color))
            self.cells.append(row)

    def draw(self, cr):
        cr.save()
        cr.translate(*self.position)

        if self.fill:
            for row in self.cells:
                for cell in row:
                    cr.set_source_rgb(*cell.color)
                    cr.rectangle(cell.x, cell.y,
                                 self.cell_size, self.cell_size)
                    cr.fill()

        cr.set_source_rgb(*Color.BLACK)
        cr.set_line_width(self.stroke)
        cr.set_font_size(self.cell_size)

        for row in self.cells:
            for cell in row:
                cr.rectangle(cell.x, cell.y, self.cell_size, self.cell_size)

        cr.stroke()

        for row in self.cells:
            for cell in row:
                cell.show_text(cr)

        cr.stroke()
        cr.restore()

    def set_position(self, dx, dy):
        self.position = dx, dy

    def update(self): pass

    def set_cell_color(self, row, col, color):
        self.cells[row][col].color = color

    def get_cell_color(self, row, col):
        return self.cells[row][col].color

    def set_cell_text(self, row, col, text):
        self.cells[row][col].text = text

    def get_cell_text(self, row, col):
        return self.cells[row][col].text

    def set_cell_text_color(self, row, col, color):
        self.cells[row][col].text_color = color

    def get_cell_text_color(self, row, col):
        return self.cells[row][col].text_color

    def get_by_position(self, x, y):
        for row in self.cells:
            for cell in row:
                if cell.is_inside(x, y):
                    return cell.row, cell.col

        return None


class MouseButtons:
    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3


class DrawingArea(Gtk.DrawingArea):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.connect("draw", self.on_draw)
        self.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)

        self.widgets = []

    def on_draw(self, wid, cr):
        cr.set_source_rgb(255, 255, 255)
        cr.rectangle(0, 0, self.width, self.height)
        cr.fill()

        for w in self.widgets:
            w.draw(cr)

    def add_widget(self, widget):
        if isinstance(widget, DrawWidget):
            self.widgets.append(widget)
