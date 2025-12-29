from components.Cell import Cell

# Board class represents the game board
class Board:
    # Initialize the board with a default size of 15x15
    def __init__(self, size=15):
        self.size = size
        # Create a 2D grid of Cell objects
        self.grid = [[Cell(r, c) for c in range(size)] for r in range(size)]

    # Check if a specific cell is empty (no stone placed)
    def is_empty(self, row, col):
        return self.grid[row][col].state is None

    # Attempt to place a stone of a given color on the board
    def place_stone(self, row, col, color):
        if self.is_empty(row, col):
            self.grid[row][col].state = color
            return True
        return False
    
    # Check if placing a stone at (row, col) results in a win
    def check_win(self, row, col, color):

        # Possible directions to check: vertical, horizontal, and two diagonals
        directions = [
            (1, 0),   # |
            (0, 1),   # _
            (1, 1),   # \
            (1, -1)   # /
        ]

        # Iterate over all directions
        for dr, dc in directions:
            count = 1  # Count the current stone

            # Check forward direction
            r, c = row + dr, col + dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c].state == color:
                count += 1
                r += dr
                c += dc

            # Check backward direction
            r, c = row - dr, col - dc
            while 0 <= r < self.size and 0 <= c < self.size and self.grid[r][c].state == color:
                count += 1
                r -= dr
                c -= dc

            # If five or more stones are aligned, the player wins
            if count >= 5:
                return True

        # No winning condition found
        return False