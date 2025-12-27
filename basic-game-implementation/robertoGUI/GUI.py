import tkinter as tk
from components.Board import Board
from AI.AI import AI

class GomokuGUI:
    def __init__(self, container=None, end_game_callback=None, mode=1, 
                 player1_name="Player", player2_name="Player 2", 
                 ai1_level=1, ai2_level=1, board_size=15, update_stones_callback=None):
        
        self.window = container if container else tk.Tk()
        # Callbacks, one for game end and one to update the stone count externally
        self.end_game_callback = end_game_callback
        self.update_stones_callback = update_stones_callback

        self.mode = mode # 1 = PvAI, 2 = PvP, 3 = AIvAI
        # Stores the last move played on the board
        self.last_move = None

        # Initialize names, levels and stones
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.ai1_level = ai1_level
        self.ai2_level = ai2_level
        self.player_stones = {"black": 60, "white": 60}

        # Initialize the game board with the selected size
        self.board = Board(board_size)
        self.size = 600 if board_size == 15 else 760

        self.pad = 40
        self.cell = (self.size - 2 * self.pad) / (board_size - 1)

        # Create the canvas where the board and stones will be drawn
        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size, bg="#F0D9B5")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        # Initialize AI players based on the selected game mode
        self.ai = [ 
                    AI(ai1_level, "black") if mode in [1, 3] else None,
                    AI(ai2_level, "white") if mode == 3 else None
                ]

        self.draw_grid()

        # Black always starts first in Gomoku
        self.current_player = "black"

        # AI are in mode 1 and mode 3
        if mode != 2:
            self.ai_first_move()

    # Destroy the game interface and release resources (used by game.py in the "Back to Menu" button while playing)
    def destroy(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.after_cancel("all")
        self.canvas.destroy()
        self.board = None
        self.ai = []

    # Only for the AI's first move
    def ai_first_move(self):
        # Start from the center of the board (standard opening move)
        row, col = self.board.size // 2, self.board.size // 2

        self.board.place_stone(row, col, "black")  
        self.draw_stone(row, col, "black")

        self.last_move = (row, col)
        self.ai[0].stones -= 1

        # Update external UI elements showing remaining stones
        if self.update_stones_callback:
            if self.mode == 1:
                p1_count = self.ai[0].stones
                p2_count = self.player_stones["white"]
            elif self.mode == 3:
                p1_count = self.ai[0].stones
                p2_count = self.ai[1].stones
            self.update_stones_callback(p1_count, p2_count)

        self.switch_player()

        # In AI vs AI mode, schedule the next AI move with a small delay
        if self.mode == 3:
            self.window.after(2000, self.ai_turn, 1)

    # Draw the Gomoku grid on the canvas
    def draw_grid(self):
        for i in range(self.board.size):
            p = self.pad + i * self.cell
            self.canvas.create_line(p, self.pad, p, self.size - self.pad)
            self.canvas.create_line(self.pad, p, self.size - self.pad, p)

    # Draw a stone on the canvas at a given board position
    def draw_stone(self, row, col, color):
        # Convert board coordinates to canvas coordinates
        x = self.pad + col * self.cell
        y = self.pad + row * self.cell
        r = self.cell * 0.45
        
        # Set stone appearance depending on color
        fill = "black" if color == "black" else "white"
        outline = "black" if color == "white" else ""
        
        # Draw the stone as a circle
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline)

        # Update stone count for human players when applicable
        if self.mode == 2 or (self.mode == 1 and color == "white"):
            self.player_stones[color] -= 1

        # Update external UI elements showing remaining stones
        if self.update_stones_callback:
            if self.mode == 1:
                p1_count = self.ai[0].stones
                p2_count = self.player_stones["white"]
            elif self.mode == 2:
                p1_count = self.player_stones["black"]
                p2_count = self.player_stones["white"]
            else:
                p1_count = self.ai[0].stones
                p2_count = self.ai[1].stones
            self.update_stones_callback(p1_count, p2_count)

        # Check end-game conditions based on remaining stones
        if self.mode == 1 and self.player_stones["white"] <= 0:
            self.end_game(f"AI won! ({self.player1_name} ran out of stones)")
        elif self.mode == 2:
            if self.player_stones["black"] <= 0:
                self.end_game(f"{self.player2_name} won! ({self.player1_name} ran out of stones)")
            elif self.player_stones["white"] <= 0:
                self.end_game(f"{self.player1_name} won! ({self.player2_name} ran out of stones)")

    # Return the display name of a player based on color and game mode
    # In the AIvAI mode, the AI's names are "AI 1" and "AI 2"
    def get_name(self, player):
        if player == "black":
            if self.mode == 1:
                return "AI"
            elif self.mode == 2:
                return self.player1_name
            else:
                return "AI 1"
        else:
            if self.mode == 1:
                return self.player1_name
            elif self.mode == 2:
                return self.player2_name
            else:
                return "AI 2"

    # Switch the current player after a valid move
    def switch_player(self):
        self.current_player = "white" if self.current_player == "black" else "black"

    # Handle mouse click events on the board
    def on_click(self, event):
        # Ignore clicks in AI vs AI mode (no humans are playing)
        if self.mode == 3:
            return

        # Convert mouse coordinates to board indices
        col = int(round((event.x - self.pad) / self.cell))
        row = int(round((event.y - self.pad) / self.cell))

        # Ignore clicks outside the board boundaries
        if row < 0 or row >= self.board.size or col < 0 or col >= self.board.size:
            return

        # Ignore the click if the cell is occupied
        if not self.board.place_stone(row, col, self.current_player):
            return
        
        self.draw_stone(row, col, self.current_player)

        # Check if the current move ends the game
        if self.board.check_win(row, col, self.current_player):
            self.end_game(f"{self.get_name(self.current_player)} won!")
            return
        
        self.switch_player()

        # In PvAI mode, schedule the AI response move
        if self.mode == 1:
            self.last_move = (row, col)
            self.window.after(100, self.ai_turn, 0)

    # Handle a full turn played by an AI player
    def ai_turn(self, ai_n: int):
        # If there is no previous move, the AI cannot make a decision
        if self.last_move is None:
            return

        # Ask the AI for the best move based on the current board state
        best_move = self.ai[ai_n].get_best_move(self.board, self.ai[ai_n].color)
        if best_move is None:
            # No valid moves left, the game ends in a draw
            self.end_game("Draw")
            return

        # Store and apply the chosen move
        row, col = best_move
        self.last_move = (row, col)

        # Safety check: ensure the move is valid on the board
        if not self.board.place_stone(row, col, self.ai[ai_n].color):
            print("AI tried invalid move:", row, col)
            return

        self.draw_stone(row, col, self.ai[ai_n].color)
        self.ai[ai_n].stones -= 1

        # Update external UI stone counters
        if self.update_stones_callback:
            if self.mode == 1:
                p1_count = self.ai[0].stones
                p2_count = self.player_stones["white"]
            elif self.mode == 3:
                p1_count = self.ai[0].stones
                p2_count = self.ai[1].stones
            self.update_stones_callback(p1_count, p2_count)

        # Check end conditions related to running out of stones
        if self.mode == 1 and self.ai[0].stones <= 0:
            self.end_game(f"{self.player1_name} won! (AI ran out of stones)")
        elif self.mode == 3:
            if self.ai[0].stones <= 0:
                self.end_game("AI 2 won! (AI 1 ran out of stones)")
            elif self.ai[1].stones <= 0:
                self.end_game("AI 1 won! (AI 2 ran out of stones)")

        # Win check
        if self.board.check_win(row, col, self.ai[ai_n].color):
            self.end_game(f"{self.get_name(self.ai[ai_n].color)} won!")

        self.switch_player()

        # In AIvAI mode, schedule the next AI turn with a delay
        if self.mode == 3:
            self.window.after(2001, self.ai_turn, 0 if ai_n == 1 else 1)

    # Start the Tkinter main loop
    def run_in_frame(self):
        if isinstance(self.window, tk.Tk):
            self.window.mainloop()

    # End the game and display a win message on the board
    def end_game(self, text):
        # Disable further user interaction
        self.canvas.unbind("<Button-1>")
        
        # Display the result text in the center of the board
        self.canvas.create_text(
            self.size // 2,
            self.size // 2,
            text=text,
            font=("Arial", 32),
            fill="red"
        )
        # Notify external components about the game result after a short delay
        if self.end_game_callback:
            winner = 1 if self.current_player == "black" else 2
            self.canvas.after(1500, lambda: self.end_game_callback(winner))