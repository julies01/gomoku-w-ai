import tkinter as tk
from GUI import GomokuGUI

class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gomoku")
        self.window.geometry("600x600")
        self.window.configure(bg="#2C3E50")

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

    # --- MENU STATE ---        
    def show_menu(self):
        self.clear_window()
        self.current_state = "menu"
        title = tk.Label(self.window, text="GOMOKU", font=("Arial", 36, "bold"), fg="#ECF0F1", bg="#2C3E50")
        title.pack(pady=40)

        self.styled_button("Play", self.ask_rules_before_play).pack(pady=15)
        self.styled_button("Options", self.show_options).pack(pady=15)
        self.styled_button("Exit game", self.window.destroy).pack(pady=15)

    # --- OPTIONS STATE --- (i just created the state but it's empty for now)
    def show_options(self):
        self.clear_window()
        self.current_state = "options"
        title = tk.Label(self.window, text="OPTIONS", font=("Arial", 28, "bold"), fg="#ECF0F1", bg="#2C3E50")
        title.pack(pady=50)
        self.styled_button("Back to Menu", self.show_menu).pack(pady=20)


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


    # --- GAME STATE ---
    def show_game(self):
        self.clear_window()
        self.current_state = "play"

        self.gomoku_frame = tk.Frame(self.window, width=600, height=600, bg="#BDC3C7")
        self.gomoku_frame.pack()

        self.gomoku = GomokuGUI(container=self.gomoku_frame, end_game_callback=self.return_to_menu)
        self.gomoku.run_in_frame()

    def return_to_menu(self):
        self.show_menu()


if __name__ == "__main__":
    Game()