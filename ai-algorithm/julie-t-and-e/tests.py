
from components import Board
import checks

"""
Test function to validate win horizontally.
"""

def test_1():
    board = Board(15)
    board.coordinates_setter()
    board.grid[7][7].state = 'black'
    board.grid[7][8].state = 'black'
    board.grid[7][9].state = 'black'
    board.grid[7][10].state = 'black'
    board.grid[7][11].state = 'black'       

    board.third_display()
    print(checks.win('black', (7,9), board))

"""
Test function to validate win vertically.
"""

def test_2():
    board = Board(15)
    board.coordinates_setter()
    board.grid[6][7].state = 'black'
    board.grid[7][7].state = 'black'
    board.grid[8][7].state = 'black'
    board.grid[9][7].state = 'black'
    board.grid[10][7].state = 'black'       

    board.third_display()
    print(checks.win('black', (8,7), board))

"""
Test function to validate win diagonally \
"""

def test_3():
    board = Board(15)
    board.coordinates_setter()
    board.grid[8][7].state = 'black'
    board.grid[9][8].state = 'black'
    board.grid[10][9].state = 'black'
    board.grid[11][10].state = 'black'
    board.grid[12][11].state = 'black'

    board.third_display()
    print(checks.win('black', (8,7), board))

"""
Test function to validate win diagonally /
"""


def test_4():
    board = Board(15)
    board.coordinates_setter()
    board.grid[7][6].state = 'black'
    board.grid[6][7].state = 'black'
    board.grid[5][8].state = 'black'
    board.grid[4][9].state = 'black'
    board.grid[3][10].state = 'black'

    board.third_display()
    print(checks.win('black', (6,7), board))

"""
    Test function to validate adjacency tables.
"""

def test_around():
    board = Board(15)
    board.coordinates_setter()
    board.grid[8][7].state = 'black'
    board.grid[9][8].state = 'black'
    board.grid[10][9].state = 'black'
    board.grid[11][10].state = 'black'

    board.grid[3][10].state = 'white'
    board.grid[4][9].state = 'white'
    board.grid[5][8].state = 'white'
    board.grid[6][7].state = 'white'
   
    return board

#test_1()
#test_2()
#test_3()
#test_4()


