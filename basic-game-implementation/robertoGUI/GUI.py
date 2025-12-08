import tkinter as tk
from components.Board import Board
from AI.AI import AI

class GomokuGUI:

    def __init__(self, container=None, end_game_callback=None):
        self.window = container if container else tk.Tk()
        self.end_game_callback = end_game_callback

        self.board = Board(15)
        self.ai = AI(level=1)
        self.ai.set_tables(self.board)

        self.size = 600
        self.cell = self.size // self.board.size
        self.last_move = None

        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size, bg="#F0D9B5")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_grid()
        self.ai_first_move()

    def ai_first_move(self):
        # this is just cuz in the CLI code the ai begins first, i needed it to test if the AI works in the same way here (it does :D)
        row, col = self.board.size // 2, self.board.size // 2

        self.board.place_stone(row, col, "black")  
        self.draw_stone(row, col, "black")

        self.ai.update_black_around(self.board, row, col)

        self.last_move = (row, col)


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

    def on_click(self, event):
        col = event.x // self.cell
        row = event.y // self.cell

        if not self.board.place_stone(row, col, "white"):
            return
        self.draw_stone(row, col, "white")

        self.ai.update_white_around(self.board, row, col)

        if self.board.check_win(row, col, "white"):
            self.end_game("You won!")
            return

        self.last_move = (row, col)
        self.window.after(100, self.ai_turn)


    def ai_turn(self):
        if self.last_move is None:
            return

        best_move = self.ai.get_best_move(self.board, self.ai.color)
        if best_move is None:
            self.end_game("Draw")
            return

        row, col = best_move

        if not self.board.place_stone(row, col, self.ai.color):
            print("AI tried invalid move:", row, col)
            return

        self.draw_stone(row, col, self.ai.color)

        self.ai.update_black_around(self.board, row, col)

        self.last_move = None

        if self.board.check_win(row, col, self.ai.color):
            self.end_game("AI won!")


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