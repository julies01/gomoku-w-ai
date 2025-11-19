import re
import sys
import random
import datetime

SCG = "\033[48;2;232;173;94m"
ECG = "\033[0m"

class Player:
    #initialisation of a player : added is_ai 
    def __init__(self, name, color, is_ai=False):
        self.name = name
        self.color = color
        self.is_ai = is_ai
        self.stones = 60 
        self.creation_date = datetime.datetime.now()
    
    def __str__(self):
        return f"{self.name} ({self.color})"

class Square:

    #init a square
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.state = "unoccupied"
        

    #return true if the square is unoccupied
    def is_free(self):
        return self.state == "unoccupied"
    

    def display(self):
        if self.state == "black":
            return SCG + "  ⚫   " + ECG
        elif self.state == "white":
            return SCG + "  ⚪   " + ECG
        else:
            y,x = self.coordinates
            coord = f"({y},{x})"
            # Rendre la longueur homogène à 7 caractères
            return SCG + coord.center(7) + ECG

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
            c += str(i + 1).center(7)
        print(c)

        for i in range(self.size):
            line = str(i + 1).rjust(3) + " "
            for j in range(self.size):
                line += self.squares[(j,i)].display()
            print(line)
        print("\n")

class GameController:
    def __init__(self, board_size=15):
        self.board = Board(board_size)
        self.players = []
        self.current_player_index = 0
        self.configure_players()
    
    def configure_players(self):
        print("Gomoku Game Configuration")
        name1 = input("Enter player 1 name: ")
        name2 = "AI_Bot"
        
        if random.random() > 0.5:
            self.players.append(Player(name1, "black"))
            self.players.append(Player(name2, "white", is_ai=True))
        else:
            self.players.append(Player(name1, "white"))
            self.players.append(Player(name2, "black", is_ai=True))
        
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
        self.board.squares[coordinates].state = color
    
    def check_victory(self, coordinates, color):
        x, y = coordinates
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        for dx, dy in directions:
            counter = 1
            for i in range(1,5):
                nx, ny = x + dx*i, y + dy*i
                if (nx, ny) in self.board.squares and self.board.squares[(nx, ny)].state == color:
                    counter += 1
                else:
                    break
            for i in range(1,5):
                nx, ny = x - dx*i, y - dy*i
                if (nx, ny) in self.board.squares and self.board.squares[(nx, ny)].state == color:
                    counter += 1
                else:
                    break
            if counter >= 5:
                return True
        return False

#the evaluation function looks for all 5 squares groups and empty squares
# !! NOT OPTIMISED, MUST FIND HOW TO SELECT THE 5 GROUPS SQUARES !!
    def evaluate_board_with_empty(self, ai_color):
        #set the opponent color
        opp_color = "white" if ai_color == "black" else "black"
        directions = [(1,0),(0,1),(1,1),(1,-1)]
        board = self.board.squares
        size = self.board.size
        #dictionnary of score for all empty squares in the game ---> key of this dictionnary is coordonates
        scores = {coord:0 for coord in board if board[coord].is_free()}




        #MAIN LOOP : take all possible 5 aligned squares and calculate the score of this placement.
        for (x, y), sq in board.items():
            if sq.is_free():
                for dx, dy in directions:
                    for offset in range(-4,1):  
                        segment = []
                        coords_segment = []
                        for i in range(5):
                            nx, ny = x + dx*(offset+i), y + dy*(offset+i)
                            if 0 <= nx < size and 0 <= ny < size:
                                segment.append(board[(nx,ny)].state)
                                coords_segment.append((nx,ny))
                            else:
                                # out of board
                                segment.append(None)  
                                coords_segment.append(None)
                        if sq.state != "unoccupied": 
                            continue







                        # SCORE CALCULATION: NEED TO BE IMPROVED

                        ai_count = segment.count(ai_color)
                        opp_count = segment.count(opp_color)
                        empty_count = segment.count("unoccupied")

                        segment_score = 0

                        # score IA (attaque)
                        segment_score += [0, 10, 100, 1000, 10000][ai_count]

                        # score adversaire (défense)
                        segment_score += [0, 8, 80, 800, 9000][opp_count]

                        # bonus if segment is empty at start or end
                        if segment[0] == "unoccupied" or segment[-1] == "unoccupied":
                            segment_score += 5
                        scores[(x,y)] += segment_score
                        print(f"Debug: Case {(x,y)} segment {segment} -> +{segment_score} points")

        # select the best score
        best_move = max(scores, key=lambda k: scores[k])
        print(f"Debug: AI chooses {best_move} with score {scores[best_move]}")
        return best_move


    def ai_best_move(self, color):
        return self.evaluate_board_with_empty(color)


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
        
        if current_player.is_ai:
            move = self.ai_best_move(current_player.color)
            print(f"{current_player.name} plays at {move}")
        else:
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
                move = coordinates
                break
        
        self.place_stone(move, current_player.color)
        current_player.stones -= 1
        self.board.display_board()
        
        if self.check_victory(move, current_player.color):
            print(f"Congratulations! {current_player.name} wins!")
            return "game_over"
        if self.check_draw():
            print("Draw! No more stones available")
            return "game_over"
        
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
                print("\nGame over! Thank you for playing!\n")
                return



if __name__ == "__main__":
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
