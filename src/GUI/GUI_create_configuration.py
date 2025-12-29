import tkinter as tk
from tkinter import messagebox
from components.Board import Board
from PIL import ImageGrab
import os
import sys

class ConfigurationScreen:

    #the constructor of the class
    def __init__(self, window, board_size, on_back_to_menu,receive_loaded_config):
        self.window = window
        self.board_size = board_size
        self.on_back_to_menu = on_back_to_menu
        self.receive_loaded_config = receive_loaded_config
        
        self.size = 600 if board_size == 15 else 760
        self.cell = self.size // board_size
        self.board2D = [[None for _ in range(board_size)] for _ in range(board_size)]
        self.color_in_use = {"value": "#ffffff"}
        
        #counters for stones
        self.white_count_var = tk.IntVar(value=0)
        self.black_count_var = tk.IntVar(value=0)

        #move history for undo functionality
        self.move_history = []
        #there is currently 5 configurations saved by default
        self.nb_of_configs = 5
        
        self.setup()
    
    # Set up the GUI components
    def setup(self):
        side_ui = 220
        total_width = self.size + side_ui * 2
        total_height = self.size + 600

        self.window.geometry(f"{total_width}x{total_height}")
        self.window.configure(bg="#2C3E50")

        # Back to Menu Button
        back_button = tk.Button(self.window, text="Back to Menu", font=("Fredoka", 16), command=self.on_back_to_menu,padx=0, pady=0, borderwidth=0)
        back_button.place(x=20, y=30)
        back_button.lift()

        # Board
        frame = tk.Frame(self.window, width=self.size, height=self.size)
        frame.place(x=20, y=80)
        frame['borderwidth'] = 3
        frame['relief'] = 'raised'
        
        self.board_canvas = tk.Canvas(frame, width=self.size, height=self.size, bg="#f0d9b5")
        self.board_canvas.pack()
        self.draw_grid()
        self.board_canvas.bind("<Button-1>", self.on_click)

        # Controls
        self.setup_controls()

    # Draw the grid lines on the board
    def draw_grid(self):
        for i in range(self.board_size):
            x = i * self.cell
            self.board_canvas.create_line(x, 0, x, self.size)
            self.board_canvas.create_line(0, x, self.size, x)

    # Set up the control panel
    def setup_controls(self):
        stone_size = 40
        controls = tk.Frame(self.window, bg="#FFFFFF", relief="raised", borderwidth=3)
        controls.place(x=40 + self.size + 40, y=80)

        inner = tk.Frame(controls, bg="#FFFFFF")
        inner.pack(padx=15, pady=15)

        # White stone
        white_row = tk.Frame(inner, bg="#FFFFFF")
        white_row.pack(pady=6, anchor="w")
        white_stone = tk.Canvas(white_row, width=stone_size, height=stone_size, bd=0, highlightthickness=0, bg="#FFFFFF", cursor="hand2")
        white_stone.create_oval(4, 4, -4, -4, fill="#ffffff", outline="#000000", width=1)
        white_stone.pack(side="left")
        white_stone.bind("<Button-1>", lambda e: self.set_color("#ffffff"))
        # White stone counter
        tk.Label(white_row, textvariable=self.white_count_var, font=("Fredoka", 14), bg="#FFFFFF", fg="#000000").pack(side="left", padx=10)

        # Black stone
        black_row = tk.Frame(inner, bg="#FFFFFF")
        black_row.pack(pady=6, anchor="w")
        black_sw = tk.Canvas(black_row, width=stone_size, height=stone_size, bd=0, highlightthickness=0, bg="#FFFFFF", cursor="hand2")
        black_sw.create_oval(4, 4, -4, -4, fill="#000000", outline="#000000", width=1)
        black_sw.pack(side="left")
        black_sw.bind("<Button-1>", lambda e: self.set_color("#000000"))

        # Black stone counter
        tk.Label(black_row, textvariable=self.black_count_var, font=("Fredoka", 14), bg="#FFFFFF", fg="#000000").pack(side="left", padx=10)

        # Buttons
        tk.Button(inner, text="Undo Move", font=("Fredoka", 16), command=self.undo_move, borderwidth=0).pack(pady=10)
        tk.Button(inner, text="Reset", font=("Fredoka", 16 ), command=self.reset, borderwidth=0).pack(pady=10)
        tk.Button(inner, text="Save Configuration", font=("Fredoka", 16),command=self.save, borderwidth=0).pack(pady=10)
        tk.Button(inner, text="Run Configuration", font=("Fredoka", 16), command=self.run_configuration, borderwidth=0).pack(pady=10)

    # Set the current stone color to the stone color selected
    def set_color(self, color):
        self.color_in_use["value"] = color

    # Handle click events on the board
    def on_click(self, event):
        col = int(round((event.x - 40) / self.cell))
        row = int(round((event.y - 40) / self.cell))

        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return
        if self.board2D[row][col] == None:
            if self.color_in_use["value"] == "#ffffff":
                # Increment the white stone counter
                self.white_count_var.set(self.white_count_var.get() + 1)
                self.board2D[row][col] = 1
            else:
                # Increment the black stone counter
                self.black_count_var.set(self.black_count_var.get() + 1)
                self.board2D[row][col] = 2
            # Draw the stone on the board
            self.draw_stone(row, col, self.color_in_use["value"])
            # Record the move in history for undo functionality
            self.move_history.append((row, col, self.board2D[row][col]))

    # Draw a stone on the board at the specified row and column
    def draw_stone(self, row, col, color):
        x = 40 + col * self.cell
        y = 40 + row * self.cell
        r = self.cell * 0.45
        self.board_canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="#333")

    # Reset the board to its initial empty state
    def reset(self):
        self.move_history = []
        for r in range(self.board_size):
            for c in range(self.board_size):
                self.board2D[r][c] = None
        self.board_canvas.delete("all")
        self.draw_grid()
        self.white_count_var.set(0)
        self.black_count_var.set(0)

    # Undo the last move made on the board
    def undo_move(self):
        print(self.move_history)
        if not self.move_history:
            return
        last_move = self.move_history.pop()
        row, col, stone_type = last_move
        
        # Decrement the counter before modifying the board
        if stone_type == 1:  # white
            self.white_count_var.set(self.white_count_var.get() - 1)
        else:  # black
            self.black_count_var.set(self.black_count_var.get() - 1)
        
        # Erase the stone from the board data
        self.board2D[row][col] = None
        
        # Redraw the board
        self.board_canvas.delete("all")
        self.draw_grid()
        for r in range(self.board_size):
            for c in range(self.board_size):
                if self.board2D[r][c] is not None:
                    draw_color = "#ffffff" if self.board2D[r][c] == 1 else "#000000"
                    self.draw_stone(r, c, draw_color)

    # Verify that there is an equal number of black and white stones
    def verify_configuration(self):
        white_count = self.white_count_var.get()
        black_count = self.black_count_var.get()

        if white_count != black_count:
            messagebox.showinfo(message='The number of white stones must equal the number of black stones.')
            return False
        else :
            return True
    
    # Run the configuration by creating a Board object and placing stones
    def run_configuration(self):
        if not self.verify_configuration():
            return  
        else :
            self.board = Board(self.board_size)
            for r in range(self.board_size):
                for c in range(self.board_size):
                    if self.board2D[r][c] == 1:
                        self.board.place_stone(r, c, "white")
                    elif self.board2D[r][c] == 2:
                        self.board.place_stone(r, c, "black")
        self.receive_loaded_config(self.board, self.board_size)
        messagebox.showinfo(message="Configuration ready to be played !", detail="You can choose your game mode in the options menu.")
            
    # Capture the board image and save it as a PNG file
    def capture_board_image(self, img_filename):        
        x = self.window.winfo_rootx() + 20
        y = self.window.winfo_rooty() + 80
        x1 = x + self.size
        y1 = y + self.size

        # Adjustment for different OS scaling
        if sys.platform.startswith('win'):
            scale = 1
        elif sys.platform.startswith('darwin'):
            scale = 2  
        else:
            scale = 1
       
        x, y, x1, y1 = x * scale, y * scale, x1 * scale, y1 * scale
        
        ImageGrab.grab().crop((x, y, x1, y1)).save(img_filename)

    # Save the current configuration to a text file, along with an image of the board
    def save(self):
        if not self.verify_configuration():
            return
        else:
            os.makedirs("gomoku_config/"+ str(self.board_size), exist_ok=True)
            self.nb_of_configs += 1
            #Put the file in the right folder
            output_path = "gomoku_config/"+ str(self.board_size) + "/"
            filename = output_path + "config_" + str(self.nb_of_configs) + ".txt"
            img_filename = output_path + "config_" + str(self.nb_of_configs) + ".png"
            self.capture_board_image(img_filename)
            # Write the board configuration to a text file
            with open(filename, "w") as f:
                for r in range(self.board_size):
                    row_str = " ".join(
                        "_" if self.board2D[r][c] == None else ("1" if self.board2D[r][c] == 1 else "0")
                        for c in range(self.board_size)
                    )
                    f.write(row_str + "\n")

        messagebox.showinfo(message="Configuration saved successfully!")