import mypy_extensions
#SCG = "\033[48;2;232;173;94m"
#ECG = "\033[0m"
#gomoku
SCG=""
ECG=""

"""
 A class representing a player in the game.
"""
class Player : 

    def __init__(self, name: str ):
        self.name = name
        self.color = None
        self.stones = 60

"""
  A class representing the game board.
"""

class Board :

    def __init__(self, size: int):
        self.size : int = size
        self.grid = [[Square() for i in range(size)] for j in range(size)]
    
    """
    Sets the coordinates and numbering for each square on the board.
    """

    def coordinates_setter(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[i][j].coordinates = (i+1, j+1)
                self.grid[i][j].no = i*self.size + j + 1

    """
        Displays the board with basic square representation.
    """
    
    def one_display(self):
        print("\n")
        c = "    "
        for i in range(self.size):
            if i < 9:
                c += str(i+1) + "    "
            else:
                c += str(i+1) + "   "
        print(c)
        for i in range(self.size):
            l = ""
            if i < 9:
                l += " " + str(i+1) + " "
            else:
                l += str(i+1) + " "
            for j in range(self.size):
                l += str(self.grid[i][j].one_display()) + (SCG + "  " + ECG)
            print(l)
            print("   " + SCG + "     " * self.size + ECG)
        print("\n")

    """
        Displays the board with square numbering.
    """

    def second_display(self):
        print("\n")
        c = "    " 
        for i in range(self.size):
            if i < 9:
                c += str(i+1) + "    "
            else:
                c += str(i+1) + "   "
        print(c)
        for i in range(self.size):
            l = ""
            if i < 9:
                l += " " + str(i+1) + " "
            else:
                l += str(i+1) + " "
            for j in range(self.size):
                l += str(self.grid[i][j].second_display()) + (SCG + "  " + ECG)
            print(l)
            print("   " + SCG + "     " * self.size + ECG)
        print("\n")

    """
        Displays the board with square coordinates.
    """
    
    def third_display(self):
        print("\n")
        c = "    " 
        for i in range(self.size):
            if i < 9:
                c += str(i+1) + "      "
            else:
                c += str(i+1) + "     "
        print(c)
        for i in range(self.size):
            l = ""
            if i < 9:
                l += " " + str(i+1) + " "
            else:
                l += str(i+1) + " "
            for j in range(self.size):
                l += str(self.grid[i][j].third_display())
            print("   " + SCG + "       " * self.size + ECG)
            print("   " + SCG + "       " * self.size + ECG)
            print(l)
        print("\n")

"""
  A class representing a square on the board.  
"""

class Square : 

    def __init__(self):
        self.coordinates = (0,0)
        self.no : int = 0
        self.state = None

    """
     Displays the square based on its state, with |_| if empty.
    """

    def one_display(self):
        if self.state == None:
            return (SCG + "|_|" + ECG)
        elif self.state == 'black':
            return (SCG + " ⚫️ " + ECG)
        elif self.state == 'white':
            return (SCG + " ⚪️ " + ECG)
    
    """
     Displays the square based on its state, with it's number if empty.
    """

    def second_display(self):
        if self.state == None:
            if self.no < 10:
                return (SCG + " " + str(self.no) + " " + ECG)
            elif self.no < 100:
                return (SCG + " " + str(self.no) + ECG)
            else:
                return (SCG + str(self.no) + ECG)
        elif self.state == 'black':
            return (SCG + " ⚫️ " + ECG)
        elif self.state == 'white':
            return (SCG + " ⚪️ " + ECG)
        
    """
     Displays the square based on its state, with it's coordinates if empty.
    """

    def third_display(self):
        if self.state == None:
            coord : str = "(" + str(self.coordinates[0]) + "," + str(self.coordinates[1]) + ")"
            length_coord : int = len(coord)
            if length_coord == 5 :
                display : str = SCG + " " + coord + " " + ECG
            elif length_coord == 6 :
                display = SCG + " " + coord + ECG
            else : 
                display = SCG + coord + ECG
            return display

        elif self.state == 'black':
            return (SCG + "   ⚫️  " + ECG)
        elif self.state == 'white':
            return (SCG + "   ⚪️  " + ECG)
        
    """
        Places a stone of the given color on the square.
    """
        
    def place_stone(self, color: str):
        self.state = color

    """
        Removes the stone from the square, setting it to empty.
    """

    def remove_stone(self):
        self.state = None

    