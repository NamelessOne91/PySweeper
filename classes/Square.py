class Square:

    def __init__(self, is_mine, is_visible=False, is_flagged=False):
        self.is_mine = is_mine
        self.is_visible = is_visible
        self.is_flagged = is_flagged
        self.proximity = 0

    def show(self):
        self.is_visible = True

    def flag(self):
        self.is_flagged = not self.is_flagged

    def increment_proximity(self):
        self.proximity += 1
