import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components import Board, Player
from AI import AI
import random
import mypy_extensions
import checks
import tests

"""
 A class representing the Gomoku game.
"""

class Game :
    
    def __init__(self):
        self.players : list[Player] = []
        self.colors : list[str] = ['black', 'white']
        self.board : Board = None
        self.type_of_game : int = None
        self.starting_player : Player = None

    def display_rules(self):
        print("The rules of Gomoku are simple. \n The objective is to be the first player to get an unbroken row of five stones horizontally, " \
        "vertically, or diagonally on a 15x15 or 19x19 board. \n The player with the black stones starts first. Players take turns placing their stones on the board, and the game continues until " \
        "one player achieves this goal or none of the players have stones left.")
    
    def start_game(self):
        print("\n\n Welcome to Gomoku game ! \n")

        print("\n Would you like to be reminded of the rules ? (yes/no)")
        remind : str = input().lower()
        if remind == 'yes':
            self.display_rules()

        # TOURNAMENT MODE SELECTION
        print("TOURNAMENT MODE SELECTION")
        print("Choose tournament format:")
        print("1. Single Game (one match)")
        print("2. Best of 3 (first to 2 wins)")
        print("3. Best of 5 (first to 3 wins)")
        print("4. Custom series")
    
        tournament_choice = checks.int_in_range("\nEnter choice (1-4): ", 1, 4)
    
        if tournament_choice == 1:
            checks.tournament = checks.Tournament(1)
            print("Single Game mode selected")
        elif tournament_choice == 2:
            checks.tournament = checks.Tournament(3)
            print("Best of 3 series selected (first to 2 wins)")
        elif tournament_choice == 3:
            checks.tournament = checks.Tournament(5)
            print("Best of 5 series selected (first to 3 wins)")
        else:
            custom_series = checks.int_in_range("Enter total number of matches (odd number recommended): ", 1, 9)
            checks.tournament = checks.Tournament(custom_series)
            wins_needed = (custom_series // 2) + 1
            print(f"Custom BO{custom_series} series selected (first to {wins_needed} wins)")

        print(f"\n{checks.tournament.get_series_status()}")

        print("\n Would you like to play on a 15*15 board or a 19*19 board ?")
        board_size : int = int(input("\nEnter 15 or 19 : "))
        self.board = Board(board_size)
        self.board.coordinates_setter()

        print("\n Choose what you want to do by writing the corresponding number :" 
        "\n 1. Play with a friend " \
        "\n 2. Play with an AI \n " \
        "3. Watch two AI play against each other")
        self.type_of_game : int = checks.int_in_range("\nEnter 1, 2 or 3 : ", 1, 3)

        if self.type_of_game == 1:
            print("You chose to play with a friend.")
            self.two_player_setup()

        elif self.type_of_game == 2:
            print("You chose to play with an AI.")
            self.one_player_setup()

        elif self.type_of_game == 3:
            print("You chose to watch two AI play against each other.")
            self.two_ai_setup()

    def two_player_setup(self):
        player_1_name : str = input("\nEnter name for Player 1 : ")
        self.players.append(Player(player_1_name))
        player_2_name : str = input("Enter name for Player 2 : ")
        self.players.append(Player(player_2_name))

        self.players[0].color = random.choice(self.colors)
        if self.players[0].color == 'black':
            self.players[1].color = 'white'
        else:
            self.players[1].color = 'black'

        if self.players[0].color == 'black' :  
            self.starting_player = self.players[0]
        else : 
            self.starting_player = self.players[1]

        print ("\n Players added successfully, Board created successfully. \n" \
        + self.players[0].name + " was assigned " + self.players[0].color + " stones and " + self.players[1].name + " was assigned " + self.players[1].color + " stones. \n " \
        + self.starting_player.name + " starts first. \n" \
        "Good game " + self.players[0].name + " and " + self.players[1].name + " !")

        # Run series for two players
        self.run_game_series()

    def one_player_setup(self):
        player_name : str = input("Enter your name : ")
        self.players.append(Player(player_name))
        self.players[0].color = 'white'

        print("\n Choose AI difficulty level by writing the corresponding number :" 
        "\n 1. Easy "
        "\n 2. Medium "
        "\n 3. Hard \n ")
        ai_level_choice : int = checks.int_in_range("Enter 1, 2 or 3 : ", 1, 3)

        # Create AI player
        ai_player = Player("AI")
        ai_player.color = 'black'
        self.players.append(ai_player)
        
        self.starting_player = self.players[1]  # AI starts

        print(f"\nGame setup: {self.players[0].name} (White) vs {self.players[1].name} (Black)")
        print(f"{self.starting_player.name} starts first.")

        # Run series for player vs AI
        self.run_game_series()

    def two_ai_setup(self):
        # Create two AI players
        ai1 = Player("AI 1")
        ai1.color = 'black'
        self.players.append(ai1)
        
        ai2 = Player("AI 2") 
        ai2.color = 'white'
        self.players.append(ai2)
        
        self.starting_player = self.players[0]
        
        print(f"\nGame setup: {self.players[0].name} (Black) vs {self.players[1].name} (White)")
        print(f"{self.starting_player.name} starts first.")
        
        # Run series for AI vs AI
        self.run_game_series()

    def run_game_series(self):
        """Run multiple matches for tournament mode"""
        while not checks.tournament.is_series_over():
            print("\n" + "="*50)
            print(f"MATCH {checks.tournament.current_match} of {checks.tournament.total_matches}")
            print("="*50)
            print(checks.tournament.get_series_status())
            
            # Reset for new match
            self.board = Board(self.board.size)
            self.board.coordinates_setter()
            for player in self.players:
                player.stones = 60
            
            checks.move_history.clear_history()
            
            # Play single match based on game type
            match_result = self.play_single_match()
            
            # Update tournament standings
            if match_result == 1:  # Player 1 win
                checks.tournament.record_win(0)
                print(f"\n{self.players[0].name} wins match {checks.tournament.current_match}!")
            elif match_result == 2:  # Player 2 win
                checks.tournament.record_win(1)
                print(f"\n{self.players[1].name} wins match {checks.tournament.current_match}!")
            else:  # Draw
                print(f"\nMatch {checks.tournament.current_match} ended in a draw!")
            
            checks.tournament.current_match += 1
            
            # Check for series winner
            series_winner_idx = checks.tournament.get_series_winner()
            if series_winner_idx is not None:
                print(f"\n TOURNAMENT CHAMPION: {self.players[series_winner_idx].name}!")
                print(f"Won the BO{checks.tournament.series_type} series {checks.tournament.player_wins[series_winner_idx]}-{checks.tournament.player_wins[1-series_winner_idx]}")
                break
            
            # Check if all matches completed
            if checks.tournament.current_match > checks.tournament.total_matches:
                print("\nSeries completed! Final score:")
                print(f"{self.players[0].name}: {checks.tournament.player_wins[0]} wins")
                print(f"{self.players[1].name}: {checks.tournament.player_wins[1]} wins")
                if checks.tournament.player_wins[0] == checks.tournament.player_wins[1]:
                    print("Series ended in a tie!")
                else:
                    winner_idx = 0 if checks.tournament.player_wins[0] > checks.tournament.player_wins[1] else 1
                    print(f"Series winner: {self.players[winner_idx].name}!")
                break
            
            # Continue to next match
            if not checks.tournament.is_series_over():
                continue_series = input("\nContinue to next match? (yes/no): ").lower()
                if continue_series != 'yes':
                    print("Series abandoned.")
                    break

    def play_single_match(self):
        """Play one complete match based on game type"""
        if self.type_of_game == 1:
            # Two player match
            turn = Turn(self.players, self.board, self.starting_player)
            return turn.play_turn()
        elif self.type_of_game == 2:
            # Player vs AI match
            return self.play_ai_match()
        elif self.type_of_game == 3:
            # AI vs AI match  
            return self.play_ai_vs_ai_match()
        return 0

    def play_ai_match(self):
        """Play match between human and AI"""
        print("AI match gameplay - implementation in progress")
        # Placeholder - return random result for testing
        return random.choice([0, 1, 2])

    def play_ai_vs_ai_match(self):
        """Play match between two AIs"""
        print("AI vs AI match gameplay - implementation in progress") 
        # Placeholder - return random result for testing
        return random.choice([0, 1, 2])

    def end_game(self, outcome : int):
        if outcome == 0 :
            print("\nIt's a draw between " + self.players[0].name + " and " + self.players[1].name + "! Well played both!\n")
        elif outcome == 1 :
            print("\nCongratulations " + self.current_turn.name + "! You won the game!\n")
        exit()

    def start_directly_1(self):
        self.players.append(Player("Alice"))
        self.players.append(Player("Bob"))
        self.players[0].color = 'black'
        self.players[1].color = 'white'
        self.board = Board(15)
        self.board.coordinates_setter()
        self.current_turn = self.players[0]
        turn = Turn(self.players, self.board, self.current_turn)
        turn.play_turn()
    
    def start_directly_2(self):
        self.players.append(Player("Alice"))
        self.players[0].color = 'white'
        self.board = tests.test_around()
        self.board.third_display()  

        gomoku_AI : AI = AI(2)
        gomoku_AI.set_tables(self.board)

        gomoku_AI.update_white_around(self.board, 8, 7)
        gomoku_AI.update_white_around(self.board, 9, 8)
        gomoku_AI.update_white_around(self.board, 10, 9)
        gomoku_AI.update_white_around(self.board, 11, 10)

        gomoku_AI.update_black_around(self.board, 3, 10)
        gomoku_AI.update_black_around(self.board, 4, 9)
        gomoku_AI.update_black_around(self.board, 5, 8)
        gomoku_AI.update_black_around(self.board, 6, 7)

        gomoku_AI.display_tables(self.board)

"""
A class representing a turn in the Gomoku game.
"""

class Turn : 

    def __init__(self, players: list[Player], board: Board, starting_player: Player):
        self.players = players
        self.board = board
        self.current_turn = starting_player

    def play_turn(self):
        self.board.third_display()
        print("\nIt's " + self.current_turn.name + "'s turn. You have " + str(self.current_turn.stones) + " stones left.")

        print("Commands: 'undo', 'undo2', or coordinates like '8,8'")

        while True:
            wanted_coordinates = input("\nEnter coordinates or command: ").strip()
        
            if wanted_coordinates.lower() == 'undo':
                player_index = self.players.index(self.current_turn)
                if checks.undo_last_move(self.board, self.players):
                    self.board.third_display()
                    self.current_turn = self.players[player_index]
                    return self.play_turn()
                continue
            elif wanted_coordinates.lower() == 'undo2':
                if checks.undo_last_two_moves(self.board, self.players):
                    self.board.third_display()
                    return self.play_turn()
                continue
            elif wanted_coordinates.lower() == 'quit':
                print("Goodbye!")
                exit()

            try:
                row, col = checks.place_stone(wanted_coordinates, self.board)
                break
            except Exception as e:
                print(f"Invalid input: {e}")
                continue

        player_index = self.players.index(self.current_turn)
        checks.record_game_move(player_index, (row, col), self.current_turn.stones)
  
        self.board.grid[row][col].place_stone(self.current_turn.color)
        self.current_turn.stones -= 1

        if checks.draw(self.players):
            print("\nIt's a draw between " + self.players[0].name + " and " + self.players[1].name + "! Well played both!\n")
            return 0

        if checks.win(self.current_turn.color, (row, col), self.board):
            self.board.third_display()
            print("\nCongratulations " + self.current_turn.name + "! You won the game!\n")
            return self.players.index(self.current_turn) + 1

        if self.current_turn == self.players[0]:
            self.current_turn = self.players[1]
        else:
            self.current_turn = self.players[0]

        return self.play_turn()

# Start the game
if __name__ == "__main__":
    Game().start_game()