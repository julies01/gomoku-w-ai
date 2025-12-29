import tkinter as tk
from GUI.GUI import GomokuGUI
from GUI.GUI_create_configuration import ConfigurationScreen
from GUI.GUI_load_configuration import LoadConfigurationScreen

class Game:
    def __init__(self):
        # Initialize main Tk window and basic properties
        self.window = tk.Tk()
        self.window.title("Gomoku")
        self.window.geometry("600x600")
        self.window.configure(bg="#2C3E50")

        # Load and set application icons of various sizes
        icon_16 = tk.PhotoImage(file="gomoku_icons/gomoku_16_icon.png")
        icon_32 = tk.PhotoImage(file="gomoku_icons/gomoku_32_icon.png")
        icon_64 = tk.PhotoImage(file="gomoku_icons/gomoku_64_icon.png")
        icon_128 = tk.PhotoImage(file="gomoku_icons/gomoku_128_icon.png")
        icon_256 = tk.PhotoImage(file="gomoku_icons/gomoku_256_icon.png")

        self.window.iconphoto(False, icon_256, icon_128, icon_64, icon_32, icon_16)

        # Default game settings
        self.mode = 1  # 1 = PvAI, 2 = PvP, 3 = AIvAI
        self.name = tk.StringVar()
        self.name.set("Player")
        self.name2 = tk.StringVar()
        self.name2.set("Player 2")
        self.aiLevel = 1
        self.aiLevel2 = 1
        self.board = 15
        self.best_of = 1
        self.scores = {"player1": 0, "player2": 0}

        # State tracking variables
        self.current_state = None
        self.gomoku_frame = None
        self.loaded_board = None

        # Start by showing the main menu
        self.show_menu()
        self.window.mainloop()

    # Utility to clear all widgets from the window
    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # Helper to create consistently styled buttons
    def styled_button(self, text, command):
        return tk.Button(
            self.window,
            text=text,
            font=("Helvetica", 16, "bold"),
            bg="#E67E22",
            fg="white",
            activebackground="#D35400",
            activeforeground="white",
            width=20,
            height=2,
            relief="raised",
            bd=5,
            command=command
        )

    # Setter functions for AI levels, board size, and match type
    def setAiLevel(self, ai, level):
        if ai == 1:
            self.aiLevel = level
        else:
            self.aiLevel2 = level
        
    def setBoard(self, board):
        self.board = board

    def setBestOf(self, bestof):
        self.best_of = bestof

    # Update visual states of AI level buttons to reflect selection
    def updateAiButtons(self, levelButton):
        normal_colors = ["#44C90A", "#E3F42A", "#F6240D"]
        pressed_colors = ["#307005", "#8C9305", "#820303"]

        for i, but in enumerate(levelButton, start=1):
            if self.aiLevel == i:
                but.config(relief="sunken", bg=pressed_colors[i-1])
            else:
                but.config(relief="raised", bg=normal_colors[i-1])

    def updateAi2Buttons(self, levelButton):
        normal = ["#44C90A", "#E3F42A", "#F6240D"]
        pressed = ["#307005", "#8C9305", "#820303"]

        for i, b in enumerate(levelButton, start=1):
            if self.aiLevel2 == i:
                b.config(relief="sunken", bg=pressed[i-1])
            else:
                b.config(relief="raised", bg=normal[i-1])

    # Update board size buttons based on current selection
    def updatebdButtons(self, boardButton):
        normal_colors = ["#95A5A6", "#95A5A6"]
        pressed_colors = ["#F1C40F", "#F1C40F"]
        boards = [15, 19]

        for i, but in enumerate(boardButton):
            if self.board == boards[i]:
                but.config(relief="sunken", bg=pressed_colors[i], fg="black")
            else:
                but.config(relief="raised", bg=normal_colors[i], fg="white")

    # Update "best of" match buttons
    def update_best_of_buttons(self, bestOfButtons):
        normal_colors = ["#95A5A6", "#95A5A6", "#95A5A6"]
        pressed_colors = ["#F1C40F", "#F1C40F", "#F1C40F"]
        best_options = [1, 3, 5]

        for i, but in enumerate(bestOfButtons):
            if self.best_of == best_options[i]:
                but.config(relief="sunken", bg=pressed_colors[i], fg="black")
            else:
                but.config(relief="raised", bg=normal_colors[i], fg="white")

    # --- MENU STATE ---        
    def show_menu(self):
        self.window.geometry("600x600")
        self.clear_window()
        self.current_state = "menu"

        # Title label
        title = tk.Label(self.window, text="GOMOKU", font=("Arial", 36, "bold"), fg="#ECF0F1", bg="#2C3E50")
        title.pack(pady=40)

        # Main menu buttons
        self.styled_button("Play", self.ask_rules_before_play).pack(pady=15)
        self.styled_button("Options", self.show_options).pack(pady=15)
        self.styled_button("Exit game", self.window.destroy).pack(pady=15)

        # Debug info printed to console
        print("Name: ", self.name.get())
        print("Name 2: ", self.name2.get())
        print("Ai level: ", self.aiLevel)
        print("Ai2 level: ", self.aiLevel2)
        print("Board: ", self.board)
        print("Mode: ", self.mode)
        print("Best of: ", self.best_of)

    # --- RULES STATE ---
    def show_rules_screen(self):
        self.clear_window()
        self.current_state = "rules"

        # Title for rules screen
        title = tk.Label(self.window, text="GOMOKU RULES", font=("Arial", 28, "bold"), fg="#ECF0F1", bg="#2C3E50")
        title.pack(pady=20)

        # Description of the game rules
        rules_text = (
            "The rules of Gomoku are simple.\n\n"
            "The objective is to be the first player to get an unbroken row of five stones "
            "horizontally, vertically, or diagonally on a 15x15 or 19x19 board.\n\n"
            "The player with the black stones starts first. Players take turns placing their stones "
            "on the board, and the game continues until one player achieves this goal or none of the players have stones left."
        )

        rules_label = tk.Label(
            self.window, text=rules_text, font=("Helvetica", 14), fg="#ECF0F1",
            bg="#34495E", wraplength=550, justify="left", bd=5, relief="sunken"
        )
        rules_label.pack(pady=20, padx=20, fill="both", expand=False)

        # Buttons to either play or go back to menu
        self.styled_button("Play", self.show_game).pack(pady=10)
        self.styled_button("Back to Menu", self.show_menu).pack(pady=10)

    # --- ASK_RULES STATE ---
    def ask_rules_before_play(self):
        self.clear_window()
        self.current_state = "ask_rules"

        # Ask if the player wants to read the rules first
        label = tk.Label(self.window, text="Do you want to review the rules?", font=("Arial", 20), fg="#ECF0F1", bg="#2C3E50")
        label.pack(pady=50)

        # Buttons for Yes/No responses
        self.styled_button("Yes", self.show_rules_screen).pack(pady=15)
        self.styled_button("No", self.show_game).pack(pady=15)

    # --- OPTIONS STATE ---
    def show_options(self):
        # Clear the window and set the current state
        self.clear_window()
        self.current_state = "options"

        # Title for the options screen
        title = tk.Label(self.window, text="OPTIONS", font=("Arial", 28, "bold"), fg="#ECF0F1", bg="#2C3E50")
        title.pack(pady=10)

        # --- GAME MODE SELECTION ---
        mode_frame = tk.Frame(self.window, bg="#2C3E5E")
        mode_frame.pack(pady=5)

        # The options menu refreshes every time a game mode is selected, updating buttons and fields
        # to match the mode's requirements. For example, AI vs AI mode hides player name inputs since no human plays.
        # To make this mechanism work, show_options is called each time a game mode is selected,
        # that's why it clears the window with self.clear_window() in his first line, it's to refresh the interface for the new mode. 

        def set_mode(m):
            # Update game mode and refresh the options screen
            self.mode = m
            self.show_options()

        # Create buttons for different modes (PvAI, PvP, AIvAI)
        modes = [("Player vs AI", 1), ("Player vs Player", 2), ("AI vs AI", 3)]
        for text, val in modes:
            tk.Button(
                mode_frame, text=text, font=("Helvetica", 12, "bold"), width=15,
                bg="#7F8C8D" if self.mode != val else "#1ABC9C", fg="white",
                activebackground="#16A085", command=lambda v=val: set_mode(v)
            ).pack(side="left", padx=5)

        # --- Settings box ---
        box = tk.Frame(self.window, bg="#3C4E5E", bd=5, relief="sunken")
        box.pack(padx=20, pady=10, fill="both", expand=False)

        # Best-of selection
        bestOfFrame = tk.Frame(box, bg="#3C4E5E")
        bestOfFrame.pack(pady=10, anchor="center")

        bestOfButtons = [
            tk.Button(bestOfFrame, text="Best of 1", font=("Helvetica", 14, "bold"), bg="#95A5A6", fg="#2C3E50",
                    command=lambda bst = 1: (self.setBestOf(bst), self.update_best_of_buttons(bestOfButtons))),
            tk.Button(bestOfFrame, text="Best of 3", font=("Helvetica", 14, "bold"), bg="#95A5A6", fg="#2C3E50",
                    command=lambda bst = 3: (self.setBestOf(bst), self.update_best_of_buttons(bestOfButtons))),
            tk.Button(bestOfFrame, text="Best of 5", font=("Helvetica", 14, "bold"), bg="#95A5A6", fg="#2C3E50",
                    command=lambda bst = 5: (self.setBestOf(bst), self.update_best_of_buttons(bestOfButtons)))
        ]
        for b in bestOfButtons:
            b.pack(side="left", padx=5, pady=5)
        self.update_best_of_buttons(bestOfButtons)

        # Board size selection
        bf = tk.Frame(box, bg="#3C4E5E")
        bf.pack(pady=10, anchor="center")

        boardButton = [
            tk.Button(bf, text="15x15", font=("Helvetica", 14, "bold"), bg="#95A5A6", fg="#2C3E50",
                    command=lambda bd=15: (self.setBoard(bd), self.updatebdButtons(boardButton))),
            tk.Button(bf, text="19x19", font=("Helvetica", 14, "bold"), bg="#95A5A6", fg="#2C3E50",
                    command=lambda bd=19: (self.setBoard(bd), self.updatebdButtons(boardButton)))
        ]
        for b in boardButton:
            b.pack(side="left", padx=5, pady=5)
        self.updatebdButtons(boardButton)

        # --- Player or AI level configuration based on mode ---
        if self.mode == 1:
            # Player name input
            tk.Label(box, text="Player Name:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack(pady=5)
            tk.Entry(box, width=30, bd=3, textvariable=self.name).pack()

            # AI level selection
            row = tk.Frame(box, bg="#3C4E5E")
            row.pack(pady=5)
            col1 = tk.Frame(row, bg="#3C4E5E")
            col1.pack(side="left", padx=20)
            tk.Label(col1, text="AI Level:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack()
            levelButton = [
                tk.Button(col1, text="Easy", bg="#44C90A", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=1: (self.setAiLevel(1, lvl), self.updateAiButtons(levelButton))),
                tk.Button(col1, text="Medium", bg="#E3F42A", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=2: (self.setAiLevel(1, lvl), self.updateAiButtons(levelButton))),
                tk.Button(col1, text="Hard", bg="#F6240D", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=3: (self.setAiLevel(1, lvl), self.updateAiButtons(levelButton)))
            ]
            for b in levelButton: b.pack(pady=2)
            self.updateAiButtons(levelButton)

        elif self.mode == 2:
            # Names for both human players
            tk.Label(box, text="Player 1 Name:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack(pady=5)
            tk.Entry(box, width=30, bd=3, textvariable=self.name).pack()
            tk.Label(box, text="Player 2 Name:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack(pady=5)
            tk.Entry(box, width=30, bd=3, textvariable=self.name2).pack()

        else:
            # AI vs AI configuration
            row = tk.Frame(box, bg="#3C4E5E")
            row.pack(pady=5)

            # AI 1 level selection
            col1 = tk.Frame(row, bg="#3C4E5E")
            col1.pack(side="left", padx=10)
            tk.Label(col1, text="AI 1 Level:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack()
            levelAI1 = [
                tk.Button(col1, text="Easy", bg="#44C90A", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=1: (self.setAiLevel(1, lvl), self.updateAiButtons(levelAI1))),
                tk.Button(col1, text="Medium", bg="#E3F42A", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=2: (self.setAiLevel(1, lvl), self.updateAiButtons(levelAI1))),
                tk.Button(col1, text="Hard", bg="#F6240D", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=3: (self.setAiLevel(1, lvl), self.updateAiButtons(levelAI1)))
            ]
            for b in levelAI1: b.pack(pady=2)
            self.updateAiButtons(levelAI1)

            # AI 2 level selection
            col2 = tk.Frame(row, bg="#3C4E5E")
            col2.pack(side="left", padx=10)
            tk.Label(col2, text="AI 2 Level:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack()
            levelAI2 = [
                tk.Button(col2, text="Easy", bg="#44C90A", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=1: (self.setAiLevel(2, lvl), self.updateAi2Buttons(levelAI2))),
                tk.Button(col2, text="Medium", bg="#E3F42A", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=2: (self.setAiLevel(2, lvl), self.updateAi2Buttons(levelAI2))),
                tk.Button(col2, text="Hard", bg="#F6240D", fg="white", font=("Helvetica", 14, "bold"),
                        command=lambda lvl=3: (self.setAiLevel(2, lvl), self.updateAi2Buttons(levelAI2)))
            ]
            for b in levelAI2: b.pack(pady=2)
            self.updateAi2Buttons(levelAI2)

        #Those buttons allow to load or create a board configuration
        config_frame = tk.Frame(self.window, bg="#3C4E5E")
        config_frame.pack(pady=10, anchor="center")

        load_config = tk.Button(config_frame, text="Load a board configuration", font=("Fredoka", 14), borderwidth=0,bg="#95A5A6", fg="#2C3E50",
                    command=lambda: self.load_configuration())
        load_config.pack(side="left", padx=5, pady=5,anchor="s")
        create_config = tk.Button(config_frame, text="Create a board configuration", font=("Fredoka", 14), borderwidth=0,bg="#95A5A6", fg="#2C3E50",
                    command=lambda: self.create_game_configuration())
        create_config.pack(side="left", padx=5, pady=5,anchor="s")

        # Back button to return to main menu
        self.styled_button("Back to Menu", self.show_menu).pack(pady=10)

    #this function is made to ask the user what board size he wants for his custom configuration
    def create_game_configuration(self):
        self.clear_window()
        self.current_state = "create_configuration"
        self.window.geometry("600x600")

        back_button = tk.Button(self.window, text="Back to Menu", command=self.show_menu,
                                font=("Fredoka", 16),borderwidth=0)
        back_button.pack(anchor="nw", pady=30, padx=10)

        t_board_size = tk.Label(self.window, text="What board size do you want ?", font=("Fredoka", 20), fg="#ECF0F1", bg="#2C3E50")
        t_board_size.pack(pady=40)

        b_15 = tk.Button(self.window, text="15x15", font=("Fredoka", 16),  borderwidth=0, command=lambda: self.configuration(15), background='#2C3E50')
        b_15.pack(pady=10)
        b_19 = tk.Button(self.window, text="19x19", font=("Fredoka", 16), borderwidth=0, command=lambda: self.configuration(19), background='#2C3E50')
        b_19.pack(pady=10)

    #this function show the configuration creation screen
    def configuration(self, board_size):
        self.clear_window()
        self.current_state = "create_configuration"
        self.config_screen = ConfigurationScreen(self.window, board_size, self.show_menu,self.receive_loaded_config)

    #this function purposes is to load a game configuration chosen by the user
    def load_configuration(self):
        self.clear_window()
        self.current_state = "load_configuration"
        self.load_config_screen = LoadConfigurationScreen(self.window, self.show_menu, self.show_options, self.receive_loaded_config)

    #this function receive the loaded configuration from the LoadConfigurationScreen class and input it in the game
    def receive_loaded_config(self, board_config, board_size):
        self.loaded_board = board_config
        self.board = board_size
        self.show_options()

    # --- GAME STATE ---
    def show_game(self):
        # Clear window and set the current state to "play"
        self.clear_window()
        self.current_state = "play"

        # Determine board pixel size and layout dimensions
        board_px = 600 if self.board == 15 else 760
        side_ui = 220
        total_width = board_px + side_ui * 2
        total_height = board_px
        self.window.geometry(f"{total_width}x{total_height}")
        self.window.configure(bg="#2C3E50")

        root = tk.Frame(self.window, bg="#2C3E50")
        root.pack(fill="both", expand=True)

        # Left panel for player 1 info
        left = tk.Frame(root, width=side_ui, bg="#34495E", bd=2, relief="groove")
        left.pack(side="left", fill="y", padx=(10,5), pady=10)

        # Center panel for the board
        center = tk.Frame(root, width=board_px, height=board_px, bg="#F8F1E7", bd=4, relief="ridge")
        center.pack(side="left", expand=True, padx=5, pady=10)

        # Right panel for player 2 info
        right = tk.Frame(root, width=side_ui, bg="#34495E", bd=2, relief="groove")
        right.pack(side="right", fill="y", padx=(5,10), pady=10)

        # Set player labels based on mode
        if self.mode == 1:
            player1_label = "AI"
            player2_label = self.name.get()
        elif self.mode == 2:
            player1_label = self.name.get()
            player2_label = self.name2.get()
        else:
            player1_label = "AI 1"
            player2_label = "AI 2"

        # Initialize stone and score variables
        self.player1_stones_var = tk.StringVar()
        self.player2_stones_var = tk.StringVar()
        self.player1_stones_var.set(f"Stones: 60")
        self.player2_stones_var.set(f"Stones: 60")

        self.player1_score_var = tk.StringVar()
        self.player2_score_var = tk.StringVar()
        self.player1_score_var.set(f"Score: {self.scores['player1']}")
        self.player2_score_var.set(f"Score: {self.scores['player2']}")

        # Left panel widgets
        tk.Label(left, text="PLAYER 1", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#34495E").pack(pady=30)
        tk.Label(left, text=player1_label, font=("Helvetica", 16, "bold"), fg="#F1C40F", bg="#34495E").pack(pady=5)
        tk.Label(left, textvariable=self.player1_stones_var, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E").pack(pady=20)
        tk.Label(left, textvariable=self.player1_score_var, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E").pack(pady=5)

        # Right panel widgets
        tk.Label(right, text="PLAYER 2", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#34495E").pack(pady=30)
        tk.Label(right, text=player2_label, font=("Helvetica", 16, "bold"), fg="#F1C40F", bg="#34495E").pack(pady=5)
        tk.Label(right, textvariable=self.player2_stones_var, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E").pack(pady=20)
        tk.Label(right, textvariable=self.player2_score_var, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E").pack(pady=5)

        # Back button to return to main menu
        tk.Button(left, text="Back to Menu", font=("Helvetica", 12, "bold"), bg="#E67E22", fg="white",
                activebackground="#D35400", relief="raised", bd=4,
                command=lambda: (self.gomoku.destroy(), self.show_menu())).pack(side="bottom", pady=30)

        # Frame to host the Gomoku board
        self.gomoku_frame = tk.Frame(center, width=board_px, height=board_px, bg="#F8F1E7")
        self.gomoku_frame.pack(expand=True)

        # Initialize the Gomoku GUI inside the center frame
        self.gomoku = GomokuGUI(
            container=self.gomoku_frame,
            end_game_callback=self.update_scores,
            mode=self.mode,
            player1_name=self.name.get(),
            player2_name=self.name2.get(),
            ai1_level=self.aiLevel,
            ai2_level=self.aiLevel2,
            board_size=self.board,
            update_stones_callback=self.update_stones,
            loaded_board=self.loaded_board

        )
        self.loaded_board = None  # Reset loaded board after use

        self.gomoku.run_in_frame()

    # Update the displayed number of stones for both players
    def update_stones(self, p1_stones, p2_stones):
        self.player1_stones_var.set(f"Stones: {p1_stones}")
        self.player2_stones_var.set(f"Stones: {p2_stones}")

    # Update the score after a round ends
    def update_scores(self, winner):
        if winner == 1:
            self.scores["player1"] += 1
        else:
            self.scores["player2"] += 1

        self.player1_score_var.set(f"Score: {self.scores['player1']}")
        self.player2_score_var.set(f"Score: {self.scores['player2']}")

        # Check if the "best of" series is over
        needed_wins = (self.best_of // 2) + 1
        if self.scores["player1"] >= needed_wins or self.scores["player2"] >= needed_wins:
            self.window.after(500, self.end_best_of)
        else:
            # Start the next round after a short delay
            self.window.after(500, lambda: self.show_game())

    # Reset scores and return to the menu after a "best of" series ends
    def end_best_of(self):
        self.scores["player1"] = 0
        self.scores["player2"] = 0
        self.player1_score_var.set(f"Score: 0")
        self.player2_score_var.set(f"Score: 0")
        self.show_menu()

if __name__ == "__main__":
    Game()