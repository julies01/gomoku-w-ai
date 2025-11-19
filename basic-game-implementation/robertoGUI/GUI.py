import tkinter as tk
from components.Board import Board
from AI.AI import AI

class GomokuGUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gomoku")

        self.board = Board(15)
        self.ai = AI(level=1)

        self.size = 600
        self.cell = self.size // self.board.size

        self.canvas = tk.Canvas(self.window, width=self.size, height=self.size, bg="#F0D9B5")
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_grid()

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

        if self.board.place_stone(row, col, "black"):
            self.draw_stone(row, col, "black")

        if self.board.check_win(row, col, "black"):
            self.end_game("You won!")
            return

        self.ai_turn()

    def ai_turn(self):
        row, col = self.ai.choose_move(self.board)
        self.board.place_stone(row, col, "white")
        self.draw_stone(row, col, "white")

        if self.board.check_win(row, col, "white"):
            self.end_game("AI won!")

    def run(self):
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