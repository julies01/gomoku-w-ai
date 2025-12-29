# Cell class represents a single position on the game board
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.state = None # "black", "white" or None (empty cell)