from DrawingArea import *
from Color import Color

cell_map = {
    0: (0, 0), 1: (0, 1), 2: (0, 2),
    3: (1, 0), 4: (1, 1), 5: (1, 2),
    6: (2, 0), 7: (2, 1), 8: (2, 2)
}


def tp_sum(a, b):
    s = [sum(x) for x in zip(a, b)]
    return tuple(s)


class Controller:
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '']

    def __init__(self, grid):
        self.grid = grid
        self.selected = (0, 0)

    def get_selected(self):
        return self.selected

    def set_sudoku(self, sudoku):
        self.unhighlight_same()
        i = 0
        for lst in sudoku:
            j = 0
            for n in lst:
                if str(n) != '0':
                    self.grid.set_cell_text(i, j, str(n))
                    self.grid.set_cell_text_color(i, j, Color.BLACK)
                else:
                    self.grid.set_cell_text(i, j, '')
                    self.grid.set_cell_text_color(i, j, Color.BLUE)
                
                j += 1
            i += 1

        self.selected = (0, 0)
        self.highlight_same()
        self.grid.set_cell_color(*self.selected, Color.GRAY)

    def check_entry(self, row, col):
        test_entry = self.grid.get_cell_text(row, col)
        if test_entry == '':
            return False                      # if the entry is empty there is no conflict of numbers

        conflicted = False

        subgrid = 3 * (row // 3), 3 * (col // 3)

        for i in range(0, 9):
            if i != row:                                    # check if the test entry already exists in the column
                entry = self.grid.get_cell_text(i, col)
                if entry == test_entry:
                    conflicted = True
                    break

            if i != col:                                    # check if the test entry already exists in the row
                entry = self.grid.get_cell_text(row, i)
                if entry == test_entry:
                    conflicted = True
                    break

            cell = tp_sum(subgrid, cell_map[i])
            if cell != (row, col):
                entry = self.grid.get_cell_text(*cell)
                if entry == test_entry:
                    conflicted = True
                    break

        if conflicted:
            for i in range(0, 9):
                if i != row:                                    # check if the test entry already exists in the column
                    entry = self.grid.get_cell_text(i, col)
                    if entry == test_entry:
                        self.grid.set_cell_color(i, col, Color.RED)

                if i != col:                                    # check if the test entry already exists in the row
                    entry = self.grid.get_cell_text(row, i)
                    if entry == test_entry:
                        self.grid.set_cell_color(row, i, Color.RED)

                cell = tp_sum(subgrid, cell_map[i])
                if cell != (row, col):
                    entry = self.grid.get_cell_text(*cell)
                    if entry == test_entry:
                        self.grid.set_cell_color(*cell, Color.RED)

        return conflicted

    def check_new_entry(self):
        return self.check_entry(*self.selected)

    def clear_conflict(self):
        new_entry = self.grid.get_cell_text(*self.selected)

        row, col = self.selected

        subgrid = 3 * (row // 3), 3 * (col // 3)

        row_conflicts = []
        col_conflicts = []
        cell_conflicts = []

        for i in range(0, 9):
            if i != row:                                    # check if the new entry already exists in the column
                entry = self.grid.get_cell_text(i, col)
                if entry == new_entry:
                    row_conflicts.append((i, col))

            if i != col:                                    # check if the new entry already exists in the row
                entry = self.grid.get_cell_text(row, i)
                if entry == new_entry:
                    col_conflicts.append((row, i))

            cell = tp_sum(subgrid, cell_map[i])
            if cell != (row, col):
                entry = self.grid.get_cell_text(*cell)
                if entry == new_entry:
                    cell_conflicts.append(cell)

        if len(row_conflicts) == 1:
            self.grid.set_cell_color(*row_conflicts[0], Color.WHITE)

        if len(col_conflicts) == 1:
            self.grid.set_cell_color(*col_conflicts[0], Color.WHITE)

        if len(cell_conflicts) == 1:
            self.grid.set_cell_color(*cell_conflicts[0], Color.WHITE)

    def check_sudoku(self):
        numbers = [str(x) for x in range(1, 10)]

        error = False

        for i in range(0, 9):
            row_numbers = numbers.copy()
            col_numbers = numbers.copy()
            cell_numbers = numbers.copy()

            for j in range(0, 9):
                entry = self.grid.get_cell_text(i, j)
                if entry in row_numbers:
                    row_numbers.remove(entry)

                entry = self.grid.get_cell_text(j, i)
                if entry in col_numbers:
                    row_numbers.remove(entry)

                entry = self.grid.get_cell_text(
                    cell_map[i][0] + cell_map[j][0],
                    cell_map[i][1] + cell_map[j][1]
                )

                if entry in cell_numbers:
                    row_numbers.remove(entry)

            if row_numbers != [] or col_numbers != [] or cell_numbers != []:
                error = True
                break

        return error

    def highlight_same(self):
        select_entry = self.grid.get_cell_text(*self.selected)
        if select_entry == '':
            return

        for i in range(0, 9):
            for j in range(0, 9):
                entry = self.grid.get_cell_text(i, j)
                color = self.grid.get_cell_color(i, j)
                if entry == select_entry and color != Color.RED:
                    self.grid.set_cell_color(i, j, Color.GREEN)

    def unhighlight_same(self):
        select_entry = self.grid.get_cell_text(*self.selected)
        if select_entry == '':
            return

        for i in range(0, 9):
            for j in range(0, 9):
                entry = self.grid.get_cell_text(i, j)
                color = self.grid.get_cell_color(i, j)
                if entry == select_entry and color != Color.RED:
                    self.grid.set_cell_color(i, j, Color.WHITE)

    def mouse_event(self, event):
        conflicted = self.check_new_entry()
        self.unhighlight_same()

        selected = self.grid.get_by_position(event.x, event.y)
        if selected != None:
            if not conflicted:
                self.grid.set_cell_color(*self.selected, Color.WHITE)
            else:
                self.grid.set_cell_color(*self.selected, Color.RED)

            self.selected = selected
            self.highlight_same()
            self.check_new_entry()
            self.grid.set_cell_color(*self.selected, Color.GRAY)

    def key_select(self, key):
        def check_index(n):
            if n < 0:
                return 8
            if n > 8:
                return 0
            return n

        selected = None
        if key == 'Up':
            selected = check_index(self.selected[0] - 1), self.selected[1]
        elif key == 'Down':
            selected = check_index(self.selected[0] + 1), self.selected[1]
        elif key == 'Left':
            selected = self.selected[0], check_index(self.selected[1] - 1)
        elif key == 'Right':
            selected = self.selected[0], check_index(self.selected[1] + 1)
        else:
            return False

        conflicted = self.check_new_entry()
        self.unhighlight_same()

        if not conflicted:
            self.grid.set_cell_color(*self.selected, Color.WHITE)
        else:
            self.grid.set_cell_color(*self.selected, Color.RED)

        self.selected = selected
        self.highlight_same()
        self.check_new_entry()
        self.grid.set_cell_color(*self.selected, Color.GRAY)

        return True

    def keyboard_event(self, event):
        key = Gdk.keyval_name(event.keyval)
        if self.key_select(key):
            return

        if self.grid.get_cell_text_color(*self.selected) == Color.BLACK:
            return

        key = '' if key == 'space' else key
        
        self.unhighlight_same()
        self.clear_conflict()

        if key in self.numbers:
            self.grid.set_cell_text(*self.selected, key)

        self.highlight_same()
        self.check_new_entry()
        self.grid.set_cell_color(*self.selected, Color.GRAY)


class SugestionController():
    def __init__(self, sugestion_grid, sudoku_controler):
        self.sugestion_grid = sugestion_grid
        self.sudoku_controler = sudoku_controler
        self.sudoku_grid = sudoku_controler.grid

    def avaliate_selected(self):
        row, col = self.sudoku_controler.get_selected()

        test_entry = self.sudoku_grid.get_cell_text(row, col)
        if test_entry != '':
            for i in range(0, 9):
                self.sugestion_grid.set_cell_text(*cell_map[i], '')
            return

        possibilities = [str(x) for x in range(1, 10)]

        subgrid = 3 * (row // 3), 3 * (col // 3)

        for i in range(0, 9):
            cmap = cell_map[i]
            self.sugestion_grid.set_cell_text(*cmap, '')

            entry = self.sudoku_grid.get_cell_text(i, col)
            if entry in possibilities:
                possibilities.remove(entry)

            entry = self.sudoku_grid.get_cell_text(row, i)
            if entry in possibilities:
                possibilities.remove(entry)

            cell = tp_sum(subgrid, cmap)
            entry = self.sudoku_grid.get_cell_text(*cell)
            if entry in possibilities:
                possibilities.remove(entry)

        i = 0
        for n in possibilities:
            self.sugestion_grid.set_cell_text(*cell_map[i], n)
            i += 1

    def mouse_event(self, event):
        self.avaliate_selected()

    def keyboard_event(self, event):
        self.avaliate_selected()


class SudokuFile:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        sudoku = []
        with open(self.file_name, 'r') as file:
            for line in file:
                l = line.rstrip('\n').split(' ')
                sudoku.append(l)
        return sudoku

    def write(self, grid):
        with open(self.file_name, 'w') as file:
            for x in range(0, 9):
                line = ''
                for y in range(0, 9):
                    t = grid.get_cell_text(x, y)
                    t = t if t != '' else '0'
                    line += t + (' ' if y < 8 else '')
                line += '\n'
                file.write(line)
