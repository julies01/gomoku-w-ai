import tkinter as tk
from GUI import GomokuGUI

class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gomoku")
        self.window.geometry("600x600")
        self.window.configure(bg="#2C3E50")

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

        self.current_state = None
        self.gomoku_frame = None
        self.show_menu()
        self.window.mainloop()

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

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
    
    def setAiLevel(self, ai, level):
        if ai == 1:
            self.aiLevel = level
        else:
            self.aiLevel2 = level
        
    def setBoard(self, board):
        self.board = board

    def setBestOf(self, bestof):
        self.best_of = bestof

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

    def updatebdButtons(self, boardButton):
        normal_colors = ["#95A5A6", "#95A5A6"]
        pressed_colors = ["#F1C40F", "#F1C40F"]

        boards = [15, 19]

        for i, but in enumerate(boardButton):
            if self.board == boards[i]:
                but.config(relief="sunken", bg=pressed_colors[i], fg="black")
            else:
                but.config(relief="raised", bg=normal_colors[i], fg="white")

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
        title = tk.Label(self.window, text="GOMOKU", font=("Arial", 36, "bold"), fg="#ECF0F1", bg="#2C3E50")
        title.pack(pady=40)

        self.styled_button("Play", self.ask_rules_before_play).pack(pady=15)
        self.styled_button("Options", self.show_options).pack(pady=15)
        self.styled_button("Exit game", self.window.destroy).pack(pady=15)
        print("Nome: ", self.name.get())
        print("Nome 2: ", self.name2.get())
        print("Ai level: ", self.aiLevel)
        print("Ai2 level: ", self.aiLevel2)
        print("Board: ", self.board)
        print("Mode: ", self.mode)
        print("Best of: ", self.best_of)

        # --- RULES STATE ---
    def show_rules_screen(self):
        self.clear_window()
        self.current_state = "rules"
        title = tk.Label(self.window, text="GOMOKU RULES", font=("Arial", 28, "bold"), fg="#ECF0F1", bg="#2C3E50")
        title.pack(pady=20)

        rules_text = (
            "The rules of Gomoku are simple.\n\n"
            "The objective is to be the first player to get an unbroken row of five stones "
            "horizontally, vertically, or diagonally on a 15x15 or 19x19 board.\n\n"
            "The player with the black stones starts first. Players take turns placing their stones "
            "on the board, and the game continues until one player achieves this goal or none of the players have stones left."
        )

        rules_label = tk.Label(self.window, text=rules_text, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E", wraplength=550, justify="left", bd=5, relief="sunken")
        rules_label.pack(pady=20, padx=20, fill="both", expand=False)
        self.styled_button("Play", self.show_game).pack(pady=10)
        self.styled_button("Back to Menu", self.show_menu).pack(pady=10)

    # --- ASK_RULES STATE ---
    def ask_rules_before_play(self):
        self.clear_window()
        self.current_state = "ask_rules"

        label = tk.Label(self.window, text="Do you want to review the rules?", font=("Arial", 20), fg="#ECF0F1", bg="#2C3E50")
        label.pack(pady=50)

        self.styled_button("Yes", self.show_rules_screen).pack(pady=15)
        self.styled_button("No", self.show_game).pack(pady=15)

        # --- OPTIONS STATE ---
    def show_options(self):
        self.clear_window()
        self.current_state = "options"

        title = tk.Label(self.window, text="OPTIONS", font=("Arial", 28, "bold"), fg="#ECF0F1", bg="#2C3E50")
        title.pack(pady=10)

        mode_frame = tk.Frame(self.window, bg="#2C3E5E")
        mode_frame.pack(pady=5)

        def set_mode(m):
            self.mode = m
            self.show_options()

        modes = [("Player vs AI", 1), ("Player vs Player", 2), ("AI vs AI", 3)]
        for text, val in modes:
            tk.Button(
                mode_frame, text=text, font=("Helvetica", 12, "bold"), width=15,
                bg="#7F8C8D" if self.mode != val else "#1ABC9C", fg="white",
                activebackground="#16A085", command=lambda v=val: set_mode(v)
            ).pack(side="left", padx=5)

        box = tk.Frame(self.window, bg="#3C4E5E", bd=5, relief="sunken")
        box.pack(padx=20, pady=10, fill="both", expand=False)

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

        if self.mode == 1:
            tk.Label(box, text="Player Name:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack(pady=5)
            tk.Entry(box, width=30, bd=3, textvariable=self.name).pack()

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
            tk.Label(box, text="Player 1 Name:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack(pady=5)
            tk.Entry(box, width=30, bd=3, textvariable=self.name).pack()
            tk.Label(box, text="Player 2 Name:", bg="#3C4E5E", fg="white", font=("Helvetica", 16)).pack(pady=5)
            tk.Entry(box, width=30, bd=3, textvariable=self.name2).pack()

        else:
            row = tk.Frame(box, bg="#3C4E5E")
            row.pack(pady=5)

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

        self.styled_button("Back to Menu", self.show_menu).pack(pady=10)

    # --- GAME STATE ---
    def show_game(self):
        self.clear_window()
        self.current_state = "play"

        board_px = 600 if self.board == 15 else 760
        side_ui = 220
        total_width = board_px + side_ui * 2
        total_height = board_px

        self.window.geometry(f"{total_width}x{total_height}")
        self.window.configure(bg="#2C3E50")

        root = tk.Frame(self.window, bg="#2C3E50")
        root.pack(fill="both", expand=True)

        left = tk.Frame(root, width=side_ui, bg="#34495E", bd=2, relief="groove")
        left.pack(side="left", fill="y", padx=(10,5), pady=10)

        center = tk.Frame(root, width=board_px, height=board_px, bg="#F8F1E7", bd=4, relief="ridge")
        center.pack(side="left", expand=True, padx=5, pady=10)

        right = tk.Frame(root, width=side_ui, bg="#34495E", bd=2, relief="groove")
        right.pack(side="right", fill="y", padx=(5,10), pady=10)

        if self.mode == 1:
            player1_label = "AI"
            player2_label = self.name.get()
        elif self.mode == 2:
            player1_label = self.name.get()
            player2_label = self.name2.get()
        else:
            player1_label = "AI 1"
            player2_label = "AI 2"

        self.player1_stones_var = tk.StringVar()
        self.player2_stones_var = tk.StringVar()
        self.player1_stones_var.set(f"Stones: 60")
        self.player2_stones_var.set(f"Stones: 60")

        self.player1_score_var = tk.StringVar()
        self.player2_score_var = tk.StringVar()
        self.player1_score_var.set(f"Score: {self.scores['player1']}")
        self.player2_score_var.set(f"Score: {self.scores['player2']}")

        tk.Label(left, text="PLAYER 1", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#34495E").pack(pady=30)
        tk.Label(left, text=player1_label, font=("Helvetica", 16, "bold"), fg="#F1C40F", bg="#34495E").pack(pady=5)
        tk.Label(left, textvariable=self.player1_stones_var, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E").pack(pady=20)

        tk.Button(left, text="Back to Menu", font=("Helvetica", 12, "bold"), bg="#E67E22", fg="white",
                activebackground="#D35400", relief="raised", bd=4,
                command=lambda: (self.gomoku.destroy(), self.show_menu())).pack(side="bottom", pady=30)

        tk.Label(right, text="PLAYER 2", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#34495E").pack(pady=30)
        tk.Label(right, text=player2_label, font=("Helvetica", 16, "bold"), fg="#F1C40F", bg="#34495E").pack(pady=5)
        tk.Label(right, textvariable=self.player2_stones_var, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E").pack(pady=20)

        tk.Label(left, textvariable=self.player1_score_var, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E").pack(pady=5)
        tk.Label(right, textvariable=self.player2_score_var, font=("Helvetica", 14), fg="#ECF0F1", bg="#34495E").pack(pady=5)


        self.gomoku_frame = tk.Frame(center, width=board_px, height=board_px, bg="#F8F1E7")
        self.gomoku_frame.pack(expand=True)

        self.gomoku = GomokuGUI(
            container=self.gomoku_frame,
            end_game_callback=self.update_scores,
            mode=self.mode,
            player1_name=self.name.get(),
            player2_name=self.name2.get(),
            ai1_level=self.aiLevel,
            ai2_level=self.aiLevel2,
            board_size=self.board,
            update_stones_callback=self.update_stones
        )

        self.gomoku.run_in_frame()

    def update_stones(self, p1_stones, p2_stones):
        self.player1_stones_var.set(f"Stones: {p1_stones}")
        self.player2_stones_var.set(f"Stones: {p2_stones}")

    def update_scores(self, winner):
        if winner == 1:
            self.scores["player1"] += 1
        else:
            self.scores["player2"] += 1

        self.player1_score_var.set(f"Score: {self.scores['player1']}")
        self.player2_score_var.set(f"Score: {self.scores['player2']}")

        needed_wins = (self.best_of // 2) + 1
        if self.scores["player1"] >= needed_wins or self.scores["player2"] >= needed_wins:
            self.window.after(500, self.end_best_of)
        else:
            self.window.after(500, lambda: self.show_game())

    def end_best_of(self):
        self.scores["player1"] = 0
        self.scores["player2"] = 0
        self.player1_score_var.set(f"Score: 0")
        self.player2_score_var.set(f"Score: 0")
        self.show_menu()

if __name__ == "__main__":
    Game()