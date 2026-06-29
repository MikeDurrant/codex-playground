import random
import tkinter as tk
from tkinter import ttk
import unicodedata

from verbs import VERBS


APP_TITLE = "Dutch Verb Sprint"
WINDOW_SIZE = "760x520"

NORMAL_CARD = "#ffffff"
CORRECT_CARD = "#d9f7df"
WRONG_CARD = "#ffe1e1"
REVEAL_CARD = "#fff1c7"
SKIP_CARD = "#e3efff"
PAGE_BG = "#f2f6fb"
TEXT_DARK = "#243047"


class DutchVerbSprint:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(700, 480)
        self.root.configure(bg=PAGE_BG)

        self.score = 0
        self.attempts = 0
        self.streak = 0
        self.last_answers = []
        self.queue = []
        self.current_verb = None
        self.answer_finished = False

        self.build_screen()
        self.reset_session()

    def build_screen(self):
        title = tk.Label(
            self.root,
            text=APP_TITLE,
            font=("Segoe UI", 28, "bold"),
            bg=PAGE_BG,
            fg=TEXT_DARK,
        )
        title.pack(pady=(22, 6))

        subtitle = tk.Label(
            self.root,
            text="Type the Dutch infinitive for each English verb.",
            font=("Segoe UI", 11),
            bg=PAGE_BG,
            fg="#5b677a",
        )
        subtitle.pack(pady=(0, 14))

        stats_frame = tk.Frame(self.root, bg=PAGE_BG)
        stats_frame.pack(fill="x", padx=42)

        self.score_label = self.make_stat_label(stats_frame, "Score: 0")
        self.attempts_label = self.make_stat_label(stats_frame, "Attempts: 0")
        self.accuracy_label = self.make_stat_label(stats_frame, "Accuracy: 0%")
        self.streak_label = self.make_stat_label(stats_frame, "Streak: 0")

        self.card = tk.Frame(
            self.root,
            bg=NORMAL_CARD,
            highlightbackground="#d6deea",
            highlightthickness=2,
        )
        self.card.pack(fill="both", expand=True, padx=42, pady=18)

        self.prompt_label = tk.Label(
            self.card,
            text="to eat",
            font=("Segoe UI", 34, "bold"),
            bg=NORMAL_CARD,
            fg=TEXT_DARK,
        )
        self.prompt_label.pack(pady=(34, 20))

        self.answer_entry = tk.Entry(
            self.card,
            font=("Segoe UI", 20),
            justify="center",
            relief="solid",
            bd=1,
        )
        self.answer_entry.pack(ipady=8, ipadx=8, padx=90, fill="x")
        self.answer_entry.bind("<Return>", self.handle_enter)

        self.feedback_label = tk.Label(
            self.card,
            text="",
            font=("Segoe UI", 14, "bold"),
            bg=NORMAL_CARD,
            fg=TEXT_DARK,
            wraplength=560,
            justify="center",
        )
        self.feedback_label.pack(pady=(18, 8))

        buttons_frame = tk.Frame(self.card, bg=NORMAL_CARD)
        buttons_frame.pack(pady=(8, 22))

        self.check_button = ttk.Button(buttons_frame, text="Check", command=self.check_answer)
        self.check_button.grid(row=0, column=0, padx=6)

        self.next_button = ttk.Button(buttons_frame, text="Next", command=self.next_question)
        self.next_button.grid(row=0, column=1, padx=6)

        self.skip_button = ttk.Button(buttons_frame, text="Skip", command=self.skip_question)
        self.skip_button.grid(row=0, column=2, padx=6)

        self.reveal_button = ttk.Button(buttons_frame, text="Reveal answer", command=self.reveal_answer)
        self.reveal_button.grid(row=0, column=3, padx=6)

        self.reset_button = ttk.Button(buttons_frame, text="Reset Session", command=self.reset_session)
        self.reset_button.grid(row=0, column=4, padx=6)

        summary_frame = tk.Frame(self.root, bg=PAGE_BG)
        summary_frame.pack(fill="x", padx=42, pady=(0, 18))

        summary_title = tk.Label(
            summary_frame,
            text="Last 5 answers",
            font=("Segoe UI", 10, "bold"),
            bg=PAGE_BG,
            fg="#5b677a",
        )
        summary_title.pack(anchor="w")

        self.summary_label = tk.Label(
            summary_frame,
            text="No answers yet.",
            font=("Segoe UI", 10),
            bg=PAGE_BG,
            fg="#5b677a",
            anchor="w",
            justify="left",
        )
        self.summary_label.pack(fill="x")

    def make_stat_label(self, parent, text):
        label = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 11, "bold"),
            bg=PAGE_BG,
            fg=TEXT_DARK,
        )
        label.pack(side="left", expand=True)
        return label

    def reset_session(self):
        self.score = 0
        self.attempts = 0
        self.streak = 0
        self.last_answers = []
        self.queue = VERBS.copy()
        random.shuffle(self.queue)
        self.current_verb = None
        self.next_question()
        self.update_stats()
        self.update_summary()

    def next_question(self):
        if not self.queue:
            self.queue = VERBS.copy()
            random.shuffle(self.queue)

        self.current_verb = self.queue.pop(0)
        self.answer_finished = False
        self.answer_entry.config(state="normal")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.focus()
        self.check_button.config(state="normal")
        self.next_button.config(state="disabled")
        self.set_card_colour(NORMAL_CARD)
        self.prompt_label.config(text=self.current_verb["english"])
        self.feedback_label.config(text="Press Enter or click Check.", fg="#5b677a")

    def handle_enter(self, event):
        if self.answer_finished:
            self.next_question()
        else:
            self.check_answer()

    def check_answer(self):
        if self.answer_finished:
            return

        user_answer = self.answer_entry.get()
        correct_answer = self.current_verb["dutch"]

        self.attempts += 1
        if self.clean_text(user_answer) == self.clean_text(correct_answer):
            self.score += 1
            self.streak += 1
            self.queue.append(self.current_verb)
            self.show_feedback(
                f"Correct! {correct_answer} means {self.current_verb['english']}.",
                CORRECT_CARD,
                "#176b31",
            )
            self.add_summary("Correct", user_answer, correct_answer)
        else:
            self.streak = 0
            self.put_back_soon(self.current_verb)
            self.show_feedback(
                f"Not quite. The answer is: {correct_answer}",
                WRONG_CARD,
                "#9d1c1c",
            )
            self.add_summary("Wrong", user_answer, correct_answer)

        self.finish_answer()

    def skip_question(self):
        if self.answer_finished:
            self.next_question()
            return

        correct_answer = self.current_verb["dutch"]
        self.streak = 0
        self.put_back_soon(self.current_verb)
        self.show_feedback(
            f"Skipped. The answer is: {correct_answer}",
            SKIP_CARD,
            "#1f5f9f",
        )
        self.add_summary("Skipped", "-", correct_answer)
        self.finish_answer()

    def reveal_answer(self):
        if self.answer_finished:
            return

        correct_answer = self.current_verb["dutch"]
        self.streak = 0
        self.put_back_soon(self.current_verb)
        self.show_feedback(
            f"Answer revealed: {correct_answer}",
            REVEAL_CARD,
            "#8a5a00",
        )
        self.add_summary("Revealed", "-", correct_answer)
        self.finish_answer()

    def finish_answer(self):
        self.answer_finished = True
        self.answer_entry.config(state="disabled")
        self.check_button.config(state="disabled")
        self.next_button.config(state="normal")
        self.update_stats()
        self.update_summary()

    def put_back_soon(self, verb):
        position = min(random.randint(2, 5), len(self.queue))
        self.queue.insert(position, verb)

    def show_feedback(self, message, colour, text_colour):
        self.set_card_colour(colour)
        self.feedback_label.config(text=message, fg=text_colour)

    def set_card_colour(self, colour):
        self.card.config(bg=colour)
        self.prompt_label.config(bg=colour)
        self.feedback_label.config(bg=colour)
        for child in self.card.winfo_children():
            if isinstance(child, tk.Frame):
                child.config(bg=colour)

    def update_stats(self):
        if self.attempts == 0:
            accuracy = 0
        else:
            accuracy = round((self.score / self.attempts) * 100)

        self.score_label.config(text=f"Score: {self.score}")
        self.attempts_label.config(text=f"Attempts: {self.attempts}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy}%")
        self.streak_label.config(text=f"Streak: {self.streak}")

    def add_summary(self, result, user_answer, correct_answer):
        english = self.current_verb["english"]
        entry = f"{result}: {english} -> {user_answer} / {correct_answer}"
        self.last_answers.insert(0, entry)
        self.last_answers = self.last_answers[:5]

    def update_summary(self):
        if not self.last_answers:
            self.summary_label.config(text="No answers yet.")
        else:
            self.summary_label.config(text="\n".join(self.last_answers))

    def clean_text(self, text):
        text = text.strip().lower()
        normalised = unicodedata.normalize("NFD", text)
        return "".join(letter for letter in normalised if unicodedata.category(letter) != "Mn")


def main():
    root = tk.Tk()
    app = DutchVerbSprint(root)
    root.mainloop()


if __name__ == "__main__":
    main()
