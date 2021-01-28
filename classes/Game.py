from .Board import Board
from .Square import Square


class Minesweeper:

	SURROUNDINGS = ((-1, -1), (-1, 0), (-1, 1),
                   (0, -1),           (0, 1),
                   (1, -1),  (1, 0), (1, 1))

	def __init__(self, difficulty):
		self.gameover = False
		self.difficulty = difficulty
		self.board = None
		self.flags = 0
		self.squares_to_win = 0

		self._set_board()
		self._find_mine_neighbours()

	def _set_board(self):
		if self.difficulty == "easy":
			self.board = Board(10, 10, 10)
		elif self.difficulty == "medium":
			self.board = Board(15, 15, 25)
		elif self.difficulty == "hard":
			self.board = Board(15, 30, 45)

		self.flags = self.board.mines
		self.squares_to_win = self.board.clean_squares

	def _find_mine_neighbours(self):

		for r, c in self.board.pos_mines:
			for x, y in Minesweeper.SURROUNDINGS:
				riga = r + x
				colonna = c + y
				if self.check_limits(riga, colonna):
					continue
								
				self.board.field[riga][colonna].increment_proximity()

	def check_limits(self, row, column):
		return row < 0 or row > self.board.rows - 1 or column < 0 or column > self.board.columns - 1

	def check_victory(self):
		return self.squares_to_win == 0

	def decrement_squares_to_win(self):
		self.squares_to_win -= 1

	def increment_counter_mines(self):
		self.flags += 1

	def decrement_counter_mines(self):
		self.flags -= 1








