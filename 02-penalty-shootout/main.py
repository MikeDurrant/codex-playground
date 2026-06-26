import random
import tkinter as tk


class PenaltyShootoutApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚽ World Cup Penalty Shootout")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        self.directions = ["Left", "Centre", "Right"]
        self.new_game()
        self.build_screen()
        self.update_screen()

    def build_screen(self):
        self.root.configure(bg="#1f7a3a")

        title = tk.Label(
            self.root,
            text="⚽ World Cup Penalty Shootout",
            font=("Arial", 26, "bold"),
            fg="white",
            bg="#1f7a3a",
        )
        title.pack(pady=20)

        self.score_label = tk.Label(
            self.root,
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#1f7a3a",
        )
        self.score_label.pack(pady=10)

        self.round_label = tk.Label(
            self.root,
            font=("Arial", 15),
            fg="white",
            bg="#1f7a3a",
        )
        self.round_label.pack(pady=5)

        self.message_label = tk.Label(
            self.root,
            font=("Arial", 18, "bold"),
            fg="#ffe066",
            bg="#1f7a3a",
            wraplength=620,
            justify="center",
        )
        self.message_label.pack(pady=25)

        button_frame = tk.Frame(self.root, bg="#1f7a3a")
        button_frame.pack(pady=15)

        self.shot_buttons = []
        for direction in self.directions:
            button = tk.Button(
                button_frame,
                text=direction,
                font=("Arial", 16, "bold"),
                width=10,
                command=lambda choice=direction: self.take_shot(choice),
            )
            button.pack(side="left", padx=10)
            self.shot_buttons.append(button)

        self.new_game_button = tk.Button(
            self.root,
            text="New Game",
            font=("Arial", 14, "bold"),
            width=12,
            command=self.reset_game,
        )
        self.new_game_button.pack(pady=25)

    def new_game(self):
        self.player_score = 0
        self.opponent_score = 0
        self.player_shots = 0
        self.opponent_shots = 0
        self.is_player_turn = True
        self.game_over = False
        self.message = "Choose where to shoot first."

    def reset_game(self):
        self.new_game()
        self.update_screen()

    def take_shot(self, shot_direction):
        if self.game_over:
            return

        keeper_direction = random.choice(self.directions)
        is_goal = shot_direction != keeper_direction

        if self.is_player_turn:
            self.player_shots += 1
            team_name = "You"
            if is_goal:
                self.player_score += 1
        else:
            self.opponent_shots += 1
            team_name = "Opponent"
            if is_goal:
                self.opponent_score += 1

        result = "GOAL!" if is_goal else "SAVED!"
        self.message = (
            f"{team_name} shot {shot_direction}. "
            f"The goalkeeper dived {keeper_direction}. {result}"
        )

        self.check_for_winner()

        if not self.game_over:
            self.is_player_turn = not self.is_player_turn

        self.update_screen()

    def check_for_winner(self):
        if self.player_shots < 5 or self.opponent_shots < 5:
            return

        both_took_five = self.player_shots == 5 and self.opponent_shots == 5
        same_number_of_shots = self.player_shots == self.opponent_shots

        if both_took_five and self.player_score != self.opponent_score:
            self.finish_game()
            return

        if same_number_of_shots and self.player_score != self.opponent_score:
            self.finish_game()

    def finish_game(self):
        self.game_over = True

        if self.player_score > self.opponent_score:
            winner = "You win the shootout!"
        else:
            winner = "The opponent wins the shootout."

        self.message = f"{self.message}\n{winner}"

    def update_screen(self):
        self.score_label.config(
            text=f"Score: You {self.player_score} - {self.opponent_score} Opponent"
        )

        if self.game_over:
            round_text = "Shootout complete"
        elif self.player_shots < 5 or self.opponent_shots < 5:
            next_kick = max(self.player_shots, self.opponent_shots) + 1
            turn = "Your penalty" if self.is_player_turn else "Opponent penalty"
            round_text = f"Penalty {next_kick} of 5 - {turn}"
        else:
            turn = "Your penalty" if self.is_player_turn else "Opponent penalty"
            round_text = f"Sudden death - {turn}"

        self.round_label.config(text=round_text)
        self.message_label.config(text=self.message)

        button_state = "disabled" if self.game_over else "normal"
        for button in self.shot_buttons:
            button.config(state=button_state)


if __name__ == "__main__":
    window = tk.Tk()
    app = PenaltyShootoutApp(window)
    window.mainloop()
