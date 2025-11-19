import components.Board as Board
import random

class AI:

    def __init__(self, level: int):
        self.level = level
        self.color = "white"
        self.stones = 60
        self.white_around = None
        self.black_around = None

    def set_tables(self, board: Board):
        self.white_around = [[0 for _ in range(board.size)] for _ in range(board.size)]
        self.black_around = [[0 for _ in range(board.size)] for _ in range(board.size)]

    def update_white_around(self, board: Board, row: int, col: int):
        self.white_around[row][col] = "◯"
        directions = [(1,0), (0,1), (1,1), (-1,1)]
        for vertical, horizontal in directions:
            for i in range(1,5):
                for sign in [1, -1]:
                    new_x = row + i * vertical * sign
                    new_y = col + i * horizontal  * sign
                    if 0 <= new_y < board.size and 0 <= new_x < board.size:
                        if board.grid[new_x][new_y].state is None:
                            self.white_around[new_x][new_y] += 1

    def update_black_around(self, board: Board, row: int, col: int):
        self.black_around[row][col] = "●"
        directions = [(1,0), (0,1), (1,1), (-1,1)]
        for vertical, horizontal in directions:
            for i in range(1,5):
                for sign in [1, -1]:
                    new_x = row + i * vertical * sign
                    new_y = col + i * horizontal * sign
                    if 0 <= new_x < board.size and 0 <= new_y < board.size:
                        if board.grid[new_x][new_y].state is None:
                            self.black_around[new_x][new_y] += 1

    def choose_move(self, board: Board):
        empty = [(r,c) for r in range(board.size)
                       for c in range(board.size)
                       if board.grid[r][c].state is None]
        return random.choice(empty)
