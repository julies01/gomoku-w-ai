from components import Board

class AI :
    
    """
     AI class representing an artificial intelligence player in the Gomoku game.
    """

    def __init__(self, level: int):
        self.level = level
        self.color = "black"
        self.stones = 60
        self.white_around = None # Table to track number of white stones around each empty square
        self.black_around = None # Table to track number of black stones around each empty square   

    """
     Sets up the tables to track the number of adjacent stones for both colors according to the board size.
    """

    def set_tables (self, board : Board) :
        self.white_around = [[0 for i in range(board.size)] for j in range(board.size)]
        self.black_around = [[0 for i in range(board.size)] for j in range(board.size)]

    """
        Displays the tables showing the number of adjacent stones for both colors.
    """

    def display_tables (self, board : Board) :
        print("\nBlack around table : \n")
        for i in range(board.size):
            l = ""
            for j in range(board.size):
                t = self.black_around[i][j]
                if t == '●':
                    l += " " + t + " "
                elif int(t) > 0 :
                    l += " " + str(t) + " "
                elif t == 0 :
                    l += " . "
                elif int(t) > 9:
                    l += " " + str(t)
                elif int(t) > 99 :
                    l += str(t)
            print(l)
        print("\nWhite around table : \n")
        for i in range(board.size):
            l = ""
            for j in range(board.size):
                t = self.white_around[i][j]
                if t == '◯':
                    l += " " + t + " "
                elif t == 0:
                    l += " . "
                elif int(t) > 0:
                    l += " " + str(t) + " "
                elif int(t) > 9:
                    l += " " + str(t)
                elif int(t) > 99 :
                    l += str(t)
            print(l)

    """
        Updates the white stones adjacency table based on a new stone placement.
        Uses directional vectors to check in all four directions.
        Limits the search to 4 squares away from the placed stone.
    """

    def update_white_around (self, board : Board, row : int, col : int) :
        dict0 = {1 : 110, 2 : 25, 3 : 5, 4 : 1}
        dict = {1 : 1, 2 : 1, 3 : 1, 4 : 1}
        self.white_around[row][col] = '◯'
        directions = [(1,0), (0,1), (1,1), (-1,1)]
        for vertical, horizontal in directions:
              for i in range(1,5):
                new_x = row + i * vertical
                new_y = col + i * horizontal
                if (0 <= new_x < board.size) and (0 <= new_y < board.size):
                     if board.grid[new_x][new_y].state == None:
                          self.white_around[new_x][new_y] += dict[i]
                new_x = row - i * vertical
                new_y = col - i * horizontal
                if (0 <= new_x < board.size) and (0 <= new_y < board.size):
                     if board.grid[new_x][new_y].state == None:
                          self.white_around[new_x][new_y] += dict[i]

    """
        Updates the black stones adjacency table based on a new stone placement.
        Uses directional vectors to check in all four directions.
        Limits the search to 4 squares away from the placed stone.
    """

    def update_black_around (self, board : Board, row : int, col : int) :
        dict0 = {1 : 110, 2 : 25, 3 : 5, 4 : 1}
        dict = {1 : 1, 2 : 1, 3 : 1, 4 : 1}
        self.black_around[row][col] = '●'
        directions = [(1,0), (0,1), (1,1), (-1,1)]
        for vertical, horizontal in directions:
              for i in range(1,5):
                new_x = row + i * vertical
                new_y = col + i * horizontal
                if (0 <= new_x < board.size) and (0 <= new_y < board.size):
                     if board.grid[new_x][new_y].state == None:
                          self.black_around[new_x][new_y] += dict[i]
                new_x = row - i * vertical
                new_y = col - i * horizontal
                if (0 <= new_x < board.size) and (0 <= new_y < board.size):
                     if board.grid[new_x][new_y].state == None:
                          self.black_around[new_x][new_y] += dict[i]


