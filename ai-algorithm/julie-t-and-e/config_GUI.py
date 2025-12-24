import tkinter as tk
from PIL import ImageTk,Image
from turtle import color, width
from tkinter import simpledialog
import tkinter.font


root = tk.Tk()
root.title("Gomoku")
screen_height = root.winfo_screenheight()
window_height = int(screen_height * 0.9)
root.geometry(f"{window_height}x{window_height}")


def homepage(window_height):
    window = tk.Canvas(root, width=window_height, height=window_height)
    window.place(x=1, y=1)
    label = tk.Label(root, text="Configure your game here!", font=("Joystix Monospace", 24))
    label.pack(pady=20)
    b_configuration = tk.Button(root, text = "Configuration",  font=("Joystix Monospace",20), command=configuration_settings, background='#ffffff')
    b_configuration.place(x=300, y=200)

def configuration_settings():
    window = tk.Canvas(root, width=window_height, height=window_height)
    window.place(x=1, y=1)
    t_board_size = tk.Label(root, text="What board size do you want ?", font=("Joystix Monospace", 24))
    t_board_size.pack(pady=20)
    b_15 = tk.Button(root, text = "15*15",  font=("Joystix Monospace",20), command=lambda:configuration(15),background='#ffffff')
    b_15.place(x=500, y=650)
    b_19 = tk.Button(root, text = "19*19",  font=("Joystix Monospace",20), command=lambda:configuration(19), background='#ffffff')
    b_19.place(x=400, y=650)


def configuration(board_size):
    window = tk.Canvas(root, width=window_height, height=window_height)
    window.place(x=1, y=1)
    size = 600 if board_size == 15 else 760
    cell = size // board_size

    color_in_use = {"value": "#ffffff"}  # couleur courante (hex)
    # plateau
    frame = tk.Frame(root, width=size, height=size)
    frame.place(x=20, y=80)
    frame['borderwidth'] = 3
    frame['relief'] = 'raised'
    board_canvas = tk.Canvas(frame, width=size, height=size, bg="#f0d9b5")
    board_canvas.pack()

    # grille
    for i in range(board_size):
        x = i * cell
        board_canvas.create_line(x, 0, x, size)
        board_canvas.create_line(0, x, size, x)

    # état du plateau
    board = [[None for _ in range(board_size)] for _ in range(board_size)]

    def set_white():
        color_in_use["value"] = "#ffffff"

    def set_black():
        color_in_use["value"] = "#000000"

    controls = tk.Frame(root)
    controls.place(x=20 + size + 20, y=80)
    b_white = tk.Button(controls, text="White", command=set_white, bg='#ffffff', width=8)
    b_white.pack(pady=5)
    b_black = tk.Button(controls, text="Black", command=set_black, bg="#000000", fg="#ffffff", width=8)
    b_black.pack(pady=5)

    # dessine une pierre centrée dans la cellule (row, col)
    def draw_stone(row, col, color_hex):
        margin = max(4, cell // 12)
        x1 = col * cell + margin
        y1 = row * cell + margin
        x2 = (col + 1) * cell - margin
        y2 = (row + 1) * cell - margin
        board_canvas.create_oval(x1, y1, x2, y2, fill=color_hex, outline="#333")

    # handler clic
    def on_click(event):
        col = event.x // cell
        row = event.y // cell
        # vérifier bornes (sécurité)
        if not (0 <= row < board_size and 0 <= col < board_size):
            return
        if board[row][col] is None:
            board[row][col] = color_in_use["value"]
            draw_stone(row, col, board[row][col])

    board_canvas.bind("<Button-1>", on_click)


homepage(window_height=window_height)
root.mainloop()
