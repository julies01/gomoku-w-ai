import tkinter as tk
from tkinter import messagebox,ttk
from components.Board import Board
from PIL import ImageTk, Image
import os 


class LoadConfigurationScreen:

    #the constructor of the class
    def __init__(self, window, on_back_to_menu,show_options,receive_loaded_config):
        self.window = window
        self.on_back_to_menu = on_back_to_menu
        self.show_options = show_options
        self.receive_loaded_config = receive_loaded_config
        self.images = []  # Garder les références des images

        self.setup()

    #the setup of the window
    def setup(self):
        self.window.geometry("800x600")
        self.window.configure(bg="#2C3E50")

        back_button = tk.Button(self.window, text="Back to Menu", borderwidth=0, command=self.on_back_to_menu,
                                font=("Fredoka", 14))
        back_button.pack(pady=30, padx=10, anchor="w")

        self.view_configuration_panel()

    #the panel to view configurations
    def view_configuration_panel(self):
        view = ttk.Notebook(self.window)
        view.pack(expand=True, fill="both", padx=10, pady=10)

        # 15x15 Tab
        fifteen_frame = tk.Frame(view, bg="#e4e4e4")
        view.add(fifteen_frame, text="15x15 Configurations")
        self.view_configurations(fifteen_frame, 15)

        # 19x19 Tab
        nineteen_frame = tk.Frame(view, bg="#e4e4e4")
        view.add(nineteen_frame, text="19x19 Configurations")
        self.view_configurations(nineteen_frame, 19)

    #the function allows to view configurations
    def view_configurations(self, parent_frame, board_size):
        config_dir = f"gomoku_config/{board_size}"
        
        # Check if the directory exists
        if not os.path.exists(config_dir):
            tk.Label(parent_frame, text="No configurations found.", 
                     font=("Fredoka", 14), fg="#ECF0F1", bg="#2C3E50").pack(pady=20)
            return

        canvas = tk.Canvas(parent_frame, bg="#e4e4e4", highlightthickness=0)
        scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#e4e4e4")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        #Create a scrollable window because there can be many configurations
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        #List all configuration files
        config_files = [f for f in os.listdir(config_dir) if f.endswith('.txt')]
        
        if not config_files:
            tk.Label(scrollable_frame, text="No configurations found.", 
                     font=("Fredoka", 14), fg="#ECF0F1", bg="#e4e4e4").pack(pady=20)
            return
        
        #For each configuration file, create a label frame with an image and a load button
        for i, config_file in enumerate(sorted(config_files)):
            label_frame = tk.LabelFrame(scrollable_frame, text=f"Configuration {i+1}", 
                                        padx=10, pady=10, bg="#34495E", fg="#ECF0F1",
                                        font=("Fredoka", 12))
            label_frame.pack(pady=10, padx=10, fill="x")

            # Load image if exists
            img_path = config_dir + "/" + config_file.replace('.txt', '.png')
            if os.path.exists(img_path):
                img = Image.open(img_path)
                img = img.resize((150, 150))  # Resize
                config_img = ImageTk.PhotoImage(img)
                self.images.append(config_img)  # Keep a reference
                
                img_label = tk.Label(label_frame, image=config_img, bg="#34495E")
                img_label.pack(side="left", padx=10)

            # Load Button to load the configuration
            file_path = f"{config_dir}/{config_file}"
            load_button = tk.Button(label_frame, text="Load",  font=("Fredoka", 12), bg="#27AE60", fg="white", borderwidth=0,
                                    command=lambda file_path=file_path, board_size=board_size: self.load_configuration_file(file_path, board_size))
            load_button.pack(side="right", padx=10)

    #the function allows to load a configuration file
    def load_configuration_file(self, file_path, board_size):
        self.board = Board(board_size)
        with open(file_path, 'r') as f:
            # Read each line and place stones accordingly
            for r, line in enumerate(f):
                values = line.strip().split()
                for c, char in enumerate(values):
                    if char =='0':
                        self.board.place_stone(r, c, "black")
                    elif char == '1':
                        self.board.place_stone(r, c, "white")                        

        messagebox.showinfo(message='Configuration loaded successfully!', detail = "You can choose your game mode in the options menu.")
        #Call the callback function to send the loaded configuration
        self.receive_loaded_config(self.board, board_size)




