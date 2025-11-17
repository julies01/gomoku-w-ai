import re
from components import Board

"""
 A function to check if an integer input is within a specified range.
 Prompts the user until a valid input is received.
"""

def int_in_range(message, min_value, max_value):
    while True :
        entry = input(message)
        try:
            value = int(entry)
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter an integer between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input, please enter an integer.")

""" 
 A function to get a 'yes' or 'no' response from the user.
 Prompts the user until a valid input is received.
"""

def yes_no(answer):
    while True :
        entry = input(answer).lower()
        if entry in ['yes', 'no']:
            return entry
        else:
            print("Please enter 'yes' or 'no'.")

"""
 A function to handle stone placement on the board.
 Prompts the user for coordinates until a valid, empty square is selected.
"""

def place_stone(wanted_coordinates: str, board : Board ):
    row,col = coordinates_in_range(wanted_coordinates, board.size)
    row,col = square_is_empty(board, row, col)
    return (row, col)

"""
 A function to validate if the provided coordinates are in the correct format and within board range.
 Prompts the user until valid coordinates are received.
"""
def coordinates_in_range(wanted_coordinates: str, board_size: int):

    pattern = r'^\d+,\d+$'
    if re.match(pattern,wanted_coordinates):
        row : int = int(wanted_coordinates.split(',')[0])
        col : int = int(wanted_coordinates.split(',')[1])
        row -= 1
        col -= 1
        if 0 <= row < board_size and 0 <= col <  board_size :
            return (row, col)
        else :
            wanted_coordinates = input("\nPlease enter coordinates within the board size : 1 to " + str(board_size) + ".")
            return coordinates_in_range(wanted_coordinates, board_size)

    else :
        wanted_coordinates = input("Please enter the coordinates in the correct format 'row,column', for example '8,8'.")
        return coordinates_in_range(wanted_coordinates, board_size)

"""
 A function to check if a square on the board is empty.
 Prompts the user until an empty square is selected.
"""

def square_is_empty(board, row: int, col: int):
    while True :
        if board.grid[row][col].state == None :
            return (row, col)
        else :
            print("The square at (" + str(row+1) + "," + str(col+1) + ") is already occupied. Please choose another square.")
            wanted_coordinates = input("\nPlease enter coordinates within the board size : 1 to " + str(board.size) + ".")
            row, col = coordinates_in_range(wanted_coordinates, board.size)
            if row is not None and col is not None:
                return (row, col)

"""
 A function to check for a draw condition based on remaining stones of players.
"""
def draw(players : list):
    if players[0].stones == 0 and players[1].stones == 0 :
        print("\nIt's a draw between " + players[0].name + " and " + players[1].name + "! Well played both!\n")
        return True

"""
    A function to check for a win condition after a stone placement.
    Uses directional vectors to check in all four directions.
"""

def win(color : str, coordinates, board: Board):
    x, y = coordinates
    directions = [(1,0), (0,1), (1,1), (-1,1)]  # vertical, horizontal, diagonal /, diagonal \

    for vertical, horizontal in directions:
        counter = 1

        # Check in the positive direction
        for i in range(1, 5):
            new_x = x + i * vertical
            new_y = y + i * horizontal
            if (0 <= new_x < board.size) and (0 <= new_y < board.size) and (board.grid[new_x][new_y].state == color):
                counter += 1
            else:
                break

        # Check in the negative direction
        for i in range(1, 5):
            new_x = x - i * vertical
            new_y = y - i * horizontal
            if (0 <= new_x < board.size) and (0 <= new_y < board.size) and (board.grid[new_x][new_y].state == color):
                counter += 1
            else:
                break

        if counter >= 5:
            return True
        
    return False

# TOURNAMENT CLASS - COPIED FROM COMPONENTS TO AVOID IMPORT ISSUES

class Tournament:
    def __init__(self, series_type=3):
        self.series_type = series_type
        self.player_wins = [0, 0]
        self.current_match = 1
        self.total_matches = series_type
    
    def record_win(self, player_index):
        if 0 <= player_index < len(self.player_wins):
            self.player_wins[player_index] += 1
    
    def get_series_winner(self):
        wins_needed = (self.series_type // 2) + 1
        for i, wins in enumerate(self.player_wins):
            if wins >= wins_needed:
                return i
        return None
    
    def is_series_over(self):
        return self.get_series_winner() is not None or self.current_match > self.total_matches
    
    def get_series_status(self):
        wins_needed = (self.series_type // 2) + 1
        status = f"BO{self.series_type} Series - Match {self.current_match}/{self.total_matches}\n"
        status += f"Wins needed: {wins_needed}\n"
        status += f"Current wins: {self.player_wins[0]} - {self.player_wins[1]}"
        return status
    
    def reset_series(self):
        self.player_wins = [0, 0]
        self.current_match = 1

# UNDO SYSTEM - TRACKS MOVE HISTORY FOR REGRET FUNCTIONALITY

class MoveHistory:
    def __init__(self):
        self.moves = []
        self.stone_counts = []
    
    def record_move(self, player_index, coordinates, stones_before):
        """Record a move with player info and stone count"""
        self.moves.append({
            'player_index': player_index,
            'coordinates': coordinates,
            'stones_before': stones_before
        })
    
    def get_last_move(self):
        """Get the last move made, returns None if no moves"""
        return self.moves[-1] if self.moves else None
    
    def pop_last_move(self):
        """Remove and return the last move"""
        return self.moves.pop() if self.moves else None
    
    def clear_history(self):
        """Clear all move history"""
        self.moves.clear()

# Global move history instance
move_history = MoveHistory()
tournament = Tournament(1)

def record_game_move(player_index, coordinates, stones_before):
    move_history.record_move(player_index, coordinates, stones_before)

def undo_last_move(board, players):
    if len(move_history.moves) < 1:
        print("No moves to undo!")
        return False
    
    last_move = move_history.pop_last_move()
    if last_move:
        row, col = last_move['coordinates']
        player_idx = last_move['player_index']
        board.grid[row][col].remove_stone()
        players[player_idx].stones = last_move['stones_before']
        print(f"Undid {players[player_idx].name}'s move at ({row+1},{col+1})")
        return True
    return False

def undo_last_two_moves(board, players):
    if len(move_history.moves) < 2:
        print("Not enough moves to undo!")
        return False
    
    undo_last_move(board, players)
    undo_last_move(board, players)
    print("Undid last two moves")
    return True