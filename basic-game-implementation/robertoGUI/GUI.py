import tkinter as tk
from components.Board import Board
from AI.AI import AI

class GomokuGUI:
    def __init__(self, container=None, end_game_callback=None, mode=1, player1_name="Player", player2_name="Player 2", ai1_level=1, ai2_level=1, board_size=15):
        self.window = container if container else tk.Tk()
        self.end_game_callback = end_game_callback
        self.mode = mode
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.ai1_level = ai1_level
        self.ai2_level = ai2_level

        self.board = Board(board_size)
        self.size = 600 if board_size == 15 else 760
        self.cell = self.size // board_size

        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size, bg="#F0D9B5")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.ai = [ 
                    AI(ai1_level, "black") if mode in [1, 3] else None,
                    AI(ai2_level, "white") if mode == 3 else None
                ]
        
        if self.ai[0]: self.ai[0].set_tables(self.board)
        if self.ai[1]: self.ai[1].set_tables(self.board)

        self.draw_grid()

        if mode == 1:
            self.current_player = "black"
            self.ai_first_move()
        else:
            self.current_player = "black"

        if mode == 3:
            self.ai_first_move()

    def ai_first_move(self):
        row, col = self.board.size // 2, self.board.size // 2

        self.board.place_stone(row, col, "black")  
        self.draw_stone(row, col, "black")

        self.ai[0].update_black_around(self.board, row, col)

        self.last_move = (row, col)

        self.switch_player()

        if self.mode == 3:
            self.ai[1].update_black_around(self.board, row, col)
            self.window.after(100, self.ai_turn, 1)


    def draw_grid(self):
        for i in range(self.board.size):
            x = i * self.cell
            self.canvas.create_line(x, 0, x, self.size)
            self.canvas.create_line(0, x, self.size, x)

    def draw_stone(self, row, col, color):
        margin = 5
        x1 = col * self.cell + margin
        y1 = row * self.cell + margin
        x2 = (col+1)*self.cell - margin
        y2 = (row+1)*self.cell - margin
        fill = "black" if color == "black" else "white"
        self.canvas.create_oval(x1, y1, x2, y2, fill=fill)

    def get_name(self, player):
        if player == "black":
            if self.mode == 1:
                return "AI"
            elif self.mode == 2:
                return self.player1_name
            else:
                return "AI 1"
        elif self.mode == 1:
            return self.player1_name
        elif self.mode == 2:
            return self.player2_name
        else:
            return "AI 2"

    def switch_player(self):
        self.current_player = "white" if self.current_player == "black" else "black"

    def on_click(self, event):
        if self.mode == 3:
            return

        col = event.x // self.cell
        row = event.y // self.cell

        if not self.board.place_stone(row, col, self.current_player):
            return
        self.draw_stone(row, col, self.current_player)

        if self.mode == 1:
            self.ai[0].update_white_around(self.board, row, col)

        if self.board.check_win(row, col, self.current_player):
            self.end_game(f"{self.get_name(self.current_player)} won!")
            return
        
        self.switch_player()

        if self.mode == 1:
            self.last_move = (row, col)
            self.window.after(100, self.ai_turn, 0)


    def ai_turn(self, ai_n: int):
        if self.last_move is None:
            return

        best_move = self.ai[ai_n].get_best_move(self.board, self.ai[ai_n].color)
        if best_move is None:
            self.end_game("Draw")
            return

        row, col = best_move
        self.last_move = (row, col)

        if not self.board.place_stone(row, col, self.ai[ai_n].color):
            print("AI tried invalid move:", row, col)
            return

        self.draw_stone(row, col, self.ai[ai_n].color)

        if self.mode == 3:
            if ai_n == 0:
                self.ai[0].update_black_around(self.board, row, col)
                self.ai[1].update_black_around(self.board, row, col)
            else:
                self.ai[0].update_white_around(self.board, row, col)
                self.ai[1].update_white_around(self.board, row, col)
        else:
            self.ai[0].update_black_around(self.board, row, col)

        if self.board.check_win(row, col, self.ai[ai_n].color):
            self.end_game(f"{self.get_name(self.ai[ai_n].color)} won!")

        self.switch_player()

        if self.mode == 3:
            self.window.after(100, self.ai_turn, 0 if ai_n == 1 else 1)

    def run_in_frame(self):
        if isinstance(self.window, tk.Tk):
            self.window.mainloop()

    def end_game(self, text):
        self.canvas.unbind("<Button-1>")
        self.canvas.create_text(
            self.size // 2,
            self.size // 2,
            text=text,
            font=("Arial", 32),
            fill="red"
        )
        if self.end_game_callback:
            self.canvas.after(2000, self.end_game_callback)