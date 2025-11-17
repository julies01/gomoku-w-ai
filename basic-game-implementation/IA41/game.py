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

    """
     Displays the rules of Gomoku.
    """

    def display_rules(self):
        print("The rules of Gomoku are simple. \n The objective is to be the first player to get an unbroken row of five stones horizontally, " \
        "vertically, or diagonally on a 15x15 or 19x19 board. \n The player with the black stones starts first. Players take turns placing their stones on the board, and the game continues until " \
        "one player achieves this goal or none of the players have stones left.")
    
    """
     Starts the Gomoku game by setting up players, board, and game type."""

    def start_game(self):
        print("\n\n Welcome to Gomoku game ! \n")

        print("\n Would you like to be reminded of the rules ? (yes/no)")
        remind : str = input().lower()
        if remind == 'yes':
            self.display_rules()

        # TOURNAMENT MODE SELECTION - FIXED IMPLEMENTATION
 
        print("TOURNAMENT MODE SELECTION")
        print("Choose tournament format:")
        print("1. Single Game (one match)")
        print("2. Best of 3 (first to 2 wins)")
        print("3. Best of 5 (first to 3 wins)")
        print("4. Custom series")
    
        tournament_choice = checks.int_in_range("\nEnter choice (1-4): ", 1, 4)
    
        if tournament_choice == 1:
            checks.tournament = checks.Tournament(1)  # Single game
            print("Single Game mode selected")
        elif tournament_choice == 2:
            checks.tournament = checks.Tournament(3)  # BO3
            print("Best of 3 series selected (first to 2 wins)")
        elif tournament_choice == 3:
            checks.tournament = checks.Tournament(5)  # BO5
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

    """ 
        Sets up a two-player game by collecting player names and assigning colors.
    """

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

        Turn.play_turn(Turn(self.players, self.board,self.starting_player))

        while not checks.tournament.is_series_over():
            print(f"MATCH {checks.tournament.current_match} of {checks.tournament.total_matches}")
            print(checks.tournament.get_series_status())
        
            self.board = Board(self.board.size)
            self.board.coordinates_setter()
            for player in self.players:
                player.stones = 60
        
            checks.move_history.clear_history()
        
            # single
            turn = Turn(self.players, self.board, self.starting_player)
            match_result = turn.play_turn()
        
            # result
            if match_result == 1:  # player1 win
                checks.tournament.record_win(0)
                print(f"\n{self.players[0].name} wins match {checks.tournament.current_match - 1}!")
            elif match_result == 2:  # player2 win
                checks.tournament.record_win(1)
                print(f"\n{self.players[1].name} wins match {checks.tournament.current_match - 1}!")
            else:  # no winner
                print(f"\nMatch {checks.tournament.current_match - 1} ended in a draw!")
                
            checks.tournament.current_match += 1
        
            # check if end
            series_winner_idx = checks.tournament.get_series_winner()
            if series_winner_idx is not None:
                print(f"TOURNAMENT CHAMPION: {self.players[series_winner_idx].name}!")
                print(f"Won the BO{checks.tournament.series_type} series {checks.tournament.player_wins[series_winner_idx]}-{checks.tournament.player_wins[1-series_winner_idx]}")
                break
        
            # check if all games end
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
        
            # ask if continue
            if not checks.tournament.is_series_over():
                continue_series = input("\nContinue to next match? (yes/no): ").lower()
                if continue_series != 'yes':
                    print("Series abandoned.")
                    break

    """
        Sets up a one-player game against an AI by collecting player name and assigning colors.
    """

    def one_player_setup(self):

        player_name : str = input("Enter your name : ")
        self.players.append(Player(player_name))
        self.players[0].color = 'white'

        print("\n Choose AI difficulty level by writing the corresponding number :" 
        "\n 1. Easy "
        "\n 2. Medium "
        "\n 3. Hard \n ")
        ai_level_choice : int = checks.int_in_range("Enter 1, 2 or 3 : ", 1, 3)

        gomoku_AI : AI = AI(ai_level_choice)

        gomoku_AI.set_tables(self.board)    
        gomoku_AI.display_tables(self.board)


    """
         Sets up a two-AI game.
    """
    def two_ai_setup(self):
        print("work in progress")

    """
        Ends the game with the given outcome.
    """

    def end_game(self,outcome : int):
        if outcome == 0 :
            print("\nIt's a draw between " + self.players[0].name + " and " + self.players[1].name + "! Well played both!\n")
        elif outcome == 1 :
            print("\nCongratulations " + self.current_turn.name + "! You won the game!\n")
        exit()

    """
        Starts a predefined game for two people for testing purposes.
    """
    def start_directly_1(self):
        self.players.append(Player("Alice"))
        self.players.append(Player("Bob"))
        self.players[0].color = 'black'
        self.players[1].color = 'white'
        self.board = Board(15)
        self.board.coordinates_setter()
        #self.board = tests.test_3()
        self.current_turn = self.players[0]
        turn = Turn(self.players, self.board, self.current_turn)
        turn.play_turn()
    
    """
        Starts a predefined game for one player against an AI for testing purposes.
    """

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

    # SERIES GAME LOOP - PLAY MULTIPLE MATCHES
    def run_series(self):
        while not checks.tournament.is_series_over():
            print("\n" + "="*50)
            print(f"MATCH {checks.tournament.current_match} of {checks.tournament.total_matches}")
            print("="*50)
            print(checks.tournament.get_series_status())
            
            # Reset board and stones for new match
            self.board = Board(self.board.size)
            self.board.coordinates_setter()
            for player in self.players:
                player.stones = 60
            
            # Clear move history for new match
            checks.move_history.clear_history()
            
            # Play a complete match
            match_result = Turn.play_turn(Turn(self.players, self.board, self.starting_player, self.type_of_game))
            
            # Handle match result and update tournament
            if match_result == 1:  # Player 1 won
                checks.tournament.record_win(0)
                print(f"\n{self.players[0].name} wins match {checks.tournament.current_match - 1}!")
            elif match_result == 2:  # Player 2 won  
                checks.tournament.record_win(1)
                print(f"\n{self.players[1].name} wins match {checks.tournament.current_match - 1}!")
            else:  # Draw
                print(f"\nMatch {checks.tournament.current_match - 1} ended in a draw!")
                checks.tournament.current_match += 1
            
            # Check for series winner
            series_winner_idx = checks.tournament.get_series_winner()
            if series_winner_idx is not None:
                print(f"TOURNAMENT CHAMPION: {self.players[series_winner_idx].name}!")
                print(f"Won the BO{checks.tournament.series_type} series {checks.tournament.player_wins[series_winner_idx]}-{checks.tournament.player_wins[1-series_winner_idx]}")
                break
            
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
            
            # Ask to continue series
            if not checks.tournament.is_series_over():
                continue_series = input("\nContinue to next match? (yes/no): ").lower()
                if continue_series != 'yes':
                    print("Series abandoned.")
                    break

"""
A class representing a turn in the Gomoku game.
"""

class Turn : 

    def __init__(self, players: list[Player], board: Board,starting_player: Player):
        self.players = players
        self.board = board
        self.current_turn = starting_player

    """
        Handles the logic for a player's turn, including stone placement and win/draw checks.
    """

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

Game().start_game()
Game().start_directly_1()
Game().start_directly_2()
