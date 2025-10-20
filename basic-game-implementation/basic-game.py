import re
import sys
import random
import datetime

SCG = "\033[48;2;232;173;94m"
ECG = "\033[0m"


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.stones = 60 
        self.creation_date = datetime.datetime.now()  # creation timestamp
    
    # Method to format display
    def __str__(self):
        return f"{self.name} ({self.color})"

class Square:
    def __init__(self, coordinates):
        self.coordinates = coordinates  # tuple (x, y)
        self.state = "unoccupied"  # "black", "white", "unoccupied"
        
    # Check if square is free
    def is_free(self):
        return self.state == "unoccupied"
    
    def display(self):
        if self.is_free():
                coord : str = "(" + str(self.coordinates[1]) + "," + str(self.coordinates[0]) + ")"
                length_coord : int = len(coord)
                if length_coord == 5 :
                    display : str = SCG + " " + coord + " " + ECG
                elif length_coord == 6 :
                    display = SCG + " " + coord + ECG
                else : 
                    display = SCG + coord+ ECG
                return display

        elif self.state == 'black':
            return (SCG + " ⚫️ " + ECG)
        elif self.state == 'white':
            return (SCG + " ⚪️ " + ECG)
        else:
            # fallback for any unexpected state
            return SCG + "   " + ECG

class Board:
    def __init__(self, size=15):
        self.size = size
        self.squares = {}
        self.initialize_board()
        
    def initialize_board(self):
        for i in range(self.size):
             for j in range(self.size):
                self.squares[(i, j)] = Square((i, j))

    def display_board(self):
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
                l += self.squares[(i, j)].display()
            print("   " + SCG + "       " * self.size + ECG)
            print("   " + SCG + "       " * self.size + ECG)
            print(l)
        print("\n")
           


class GameController:
    def __init__(self, board_size=15):
        self.board = Board(board_size)
        self.players = []
        self.current_player_index = 0
        self.configure_players()
    
    def configure_players(self):
        # Configure players at start
        print("Gomoku Game Configuration")
        name1 = input("Enter player 1 name: ")
        name2 = input("Enter player 2 name: ")
        
        # Color assignment
        if random.random() > 0.5:
            self.players.append(Player(name1, "black"))
            self.players.append(Player(name2, "white"))
        else:
            self.players.append(Player(name1, "white"))
            self.players.append(Player(name2, "black"))
        
        print(f"\n{self.players[0].name} uses {self.players[0].color} stones ●")
        print(f"{self.players[1].name} uses {self.players[1].color} stones ○\n")
    
    def get_current_player(self):
        return self.players[self.current_player_index]
    
    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index
    
    def validate_coordinates(self, user_input):
        pattern = r'^\((\d+),(\d+)\)$'
        match = re.match(pattern, user_input)
        
        if not match:
            return None, "Error: Invalid format, use (x,y)"
        
        try:
            x = int(match.group(1))
            y = int(match.group(2))
        except ValueError:
            return None, "Error: Coordinates must be numeric"
        
        if x < 0 or x >= self.board.size or y < 0 or y >= self.board.size:
            return None, f"Error: Coordinates out of bounds (0-{self.board.size-1})"
        
        return (x, y), None
    
    def is_square_occupied(self, coordinates):
        return not self.board.squares[coordinates].is_free()
    
    def place_stone(self, coordinates, color):
        square = self.board.squares[coordinates]
        square.state = color
    
    def check_victory(self, coordinates, color):
        x, y = coordinates
        directions = [
            (1, 0),   # horizontal
            (0, 1),   # vertical  
            (1, 1),   # diagonal /
            (1, -1)   # diagonal \
        ]
        
        for dx, dy in directions:
            counter = 1  # start with placed stone
            
            # Check in one direction
            for i in range(1, 5):
                nx, ny = x + dx * i, y + dy * i
                if (nx, ny) in self.board.squares and self.board.squares[(nx, ny)].state == color:
                    counter += 1
                else:
                    break
            
            # Check in opposite direction
            for i in range(1, 5):
                nx, ny = x - dx * i, y - dy * i
                if (nx, ny) in self.board.squares and self.board.squares[(nx, ny)].state == color:
                    counter += 1
                else:
                    break
            
            ### Victory condition
            if counter >= 5:
                return True
        
        return False
    
    def check_draw(self):
        return all(player.stones == 0 for player in self.players)
    
    def surrender_game(self):
        current_player = self.get_current_player()
        print(f"{current_player.name} surrenders!")
        self.switch_player()
        winner = self.get_current_player()
        print(f"Winner: {winner.name}!")
        return "game_over"
    
    def player_turn(self):
        current_player = self.get_current_player()
        
        print(f"\n=== {current_player.name}'s turn ({current_player.color}) ===")
        print(f"Stones remaining: {current_player.stones}")
        
        while True:
            entry = input("Coordinates (x,y), 'quit', 'surrender': ").strip()
            
            if entry.lower() == 'quit':
                print("Goodbye!")
                sys.exit()
            elif entry.lower() == 'surrender':
                return self.surrender_game()
            
            coordinates, error = self.validate_coordinates(entry)
            if error:
                print(error)
                continue
            
            if self.is_square_occupied(coordinates):
                print("Square occupied - choose another position")
                continue
            
            # Place stone
            self.place_stone(coordinates, current_player.color)
            current_player.stones -= 1
            
            # Display updated board
            self.board.display_board()
            
            ### Check end conditions
            if self.check_victory(coordinates, current_player.color):
                print(f"Congratulations! {current_player.name} wins!")
                return "game_over"
            
            if self.check_draw():
                print("Draw! No more stones available")
                return "game_over"
            
            # Switch to next player
            self.switch_player()
            return "continue"
    
    def start_game(self):
        print("Gomoku Game")
        print("Available commands:")
        print("  (x,y) - place a stone")
        print("  surrender - capitulate")
        print("  quit - quit the game")
        
        self.board.display_board()
        
        while True:
            result = self.player_turn()
            
            if result == "game_over":
                print("Thank you for playing!")
                break

### Program entry point
if __name__ == "__main__":
    # Board size configuration
    while True:
        try:
            size = int(input("Board size (15 or 19, default 15): ") or "15")
            if size not in [15, 19]:
                print("Choice: 15 or 19")
                continue
            break
        except ValueError:
            print("Please enter a valid number")
    
    game = GameController(size)
    game.start_game()
