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

        Turn.play_turn(Turn(self.players, self.board,self.starting_player,self.type_of_game))

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
        Turn(self.players, self.board,self.current_turn).play_turn()
    
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

"""
 A class representing a turn in the Gomoku game."""

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

        wanted_coordinates :str = input("\nEnter the coordinates of the square where you want to place your stone, in the format row, column, for example '8,8' : ")

        row, col = checks.place_stone(wanted_coordinates, self.board)
        self.board.grid[row][col].place_stone(self.current_turn.color)
        self.current_turn.stones -= 1

        if checks.draw(self.players):
            Game.end_game(self,0)

        if checks.win(self.current_turn.color, (row, col), self.board):
            self.board.third_display()
            Game.end_game(self,1)

        else :
            if self.current_turn == self.players[0]:
                self.current_turn = self.players[1]
            else:
                self.current_turn = self.players[0]

        self.play_turn() 

#Game().start_game()
#Game().start_directly_1()
Game().start_directly_2()

