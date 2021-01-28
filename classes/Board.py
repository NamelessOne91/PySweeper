from .Square import Square
from random import randint


class Board:

    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.pos_mines = self._place_mines()
        self.clean_squares = (rows * columns) - mines
        self.field = []

        for r in range(rows):
            self.field.append([])
            for c in range(columns):
                if [r, c] in self.pos_mines:
                    temp = Square(True)
                else:
                    temp = Square(False)
                self.field[r].append(temp)

    def _place_mines(self):
        counter = 0
        mines = []
        while(counter < self.mines):
            mine = [randint(0, self.rows - 1), randint(0, self.columns - 1)]
            if mine not in mines:
                mines.append(mine)
                counter += 1
        return mines
