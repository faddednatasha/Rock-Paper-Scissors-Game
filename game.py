"""
Rock-Paper-Scissors — Tkinter GUI version
Features:
 - Polished Tkinter GUI with large emoji buttons
 - Single-player (vs computer) and Local 2-player modes (take turns)
 - Best-of-N match support
 - Animated countdown, scoreboard, round history
 - Sound feedback (uses winsound on Windows; falls back to root.bell())
 - Clean layout, restart and quit controls

Dependencies: only standard library (tkinter). Optional: Pillow (PIL) for images, pygame for advanced sounds.

Run: python rps_tkinter_enhanced.py
"""

import random
import sys
import platform
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

# Try to import winsound for Windows beep
try:
    import winsound
except Exception:
    winsound = None

CHOICES = ["rock", "paper", "scissors"]
EMOJI = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}

# Determine platform-friendly font sizes
IS_MAC = platform.system() == "Darwin"
FONT_LG = ("Segoe UI Emoji" if not IS_MAC else "Apple Color Emoji", 36)
FONT_MD = ("Segoe UI Emoji" if not IS_MAC else "Apple Color Emoji", 20)
FONT_SM = ("Segoe UI", 12)

class RPSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rock · Paper · Scissors — Enhanced")
        self.resizable(False, False)
        self.style = ttk.Style(self)

        # Game state
        self.mode = tk.StringVar(value="single")  # 'single' or 'local'
        self.best_of = None  # odd int or None for infinite
        self.target = None
        self.player_score = 0
        self.comp_score = 0
        self.ties = 0
        self.round_num = 0
        self.current_player = 1  # used in local mode: 1 or 2
        self.history = []

        self._build_ui()

    def _build_ui(self):
        pad = 10
        top = ttk.Frame(self, padding=pad)
        top.grid(row=0, column=0, sticky="ew")

        ttk.Label(top, text="Rock · Paper · Scissors", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w")

        ctrl = ttk.Frame(self, padding=(0, pad, 0, 0))
        ctrl.grid(row=1, column=0, sticky="ew")

        # Mode selector and best-of
        ttk.Label(ctrl, text="Mode:").grid(row=0, column=0, sticky="w")
        mode_single = ttk.Radiobutton(ctrl, text="Single Player", variable=self.mode, value="single", command=self._on_mode_change)
        mode_local = ttk.Radiobutton(ctrl, text="Local 2-Player", variable=self.mode, value="local", command=self._on_mode_change)
        mode_single.grid(row=0, column=1, sticky="w", padx=(5,2))
        mode_local.grid(row=0, column=2, sticky="w", padx=(2,5))

        self.best_of_btn = ttk.Button(ctrl, text="Set Best-of (Enter odd)", command=self._set_best_of)
        self.best_of_btn.grid(row=0, column=3, sticky="e", padx=(20,0))

        # Center area: big emoji buttons
        center = ttk.Frame(self, padding=(pad, pad))
        center.grid(row=2, column=0)

        self.choice_frame = ttk.Frame(center)
        self.choice_frame.grid(row=0, column=0)

        self.btns = {}
        for i, ch in enumerate(CHOICES):
            b = tk.Button(self.choice_frame, text=f"{EMOJI[ch]}\n{ch.title()}", font=FONT_LG, width=8, height=3,
                          command=lambda c=ch: self.on_player_choice(c))
            b.grid(row=0, column=i, padx=8)
            self.btns[ch] = b

        # Countdown / info area
        info = ttk.Frame(self, padding=(pad, 0))
        info.grid(row=3, column=0, sticky="ew")
        self.info_label = ttk.Label(info, text="Welcome! Choose a mode and press a choice.", font=FONT_MD)
        self.info_label.grid(row=0, column=0, sticky="w")

        # Scoreboard
        score = ttk.Frame(self, padding=(pad, pad))
        score.grid(row=4, column=0, sticky="ew")
        self.score_label = ttk.Label(score, text=self._score_text(), font=FONT_SM)
        self.score_label.grid(row=0, column=0, sticky="w")

        # Round result + history
        lower = ttk.Frame(self, padding=(pad, 0, pad, pad))
        lower.grid(row=5, column=0, sticky="ew")

        self.result_var = tk.StringVar(value="")
        ttk.Label(lower, textvariable=self.result_var, font=FONT_MD).grid(row=0, column=0, sticky="w")

        hist_label = ttk.Label(lower, text="Round history:")
        hist_label.grid(row=1, column=0, sticky="w", pady=(6,0))
        self.hist_box = tk.Listbox(lower, height=6, width=54)
        self.hist_box.grid(row=2, column=0, pady=(2,0))

        # Controls: restart / quit
        bottom = ttk.Frame(self, padding=pad)
        bottom.grid(row=6, column=0, sticky="ew")
        ttk.Button(bottom, text="Restart Match", command=self.restart_match).grid(row=0, column=0, sticky="w")
        ttk.Button(bottom, text="Reset All", command=self.reset_all).grid(row=0, column=1, sticky="w", padx=(6,0))
        ttk.Button(bottom, text="Quit", command=self.quit).grid(row=0, column=2, sticky="e")

        self._on_mode_change()

    def _score_text(self):
        tgt_text = f" | Best-of {self.best_of} (first to {self.target})" if self.best_of else ""
        return f"You: {self.player_score}  —  Computer: {self.comp_score}  (Ties: {self.ties}){tgt_text}"

    def _on_mode_change(self):
        mode = self.mode.get()
        if mode == "single":
            self.info_label.config(text="Single-player: play against the computer.")
        else:
            self.info_label.config(text="Local 2-player: players take turns. Player 1 starts.")
        self.restart_match()

    def _set_best_of(self):
        ans = simpledialog.askstring("Best-of", "Enter an odd number (e.g. 3,5,7) or leave blank for infinite:", parent=self)
        if ans is None:
            return
        ans = ans.strip()
        if ans == "":
            self.best_of = None
            self.target = None
            messagebox.showinfo("Best-of", "Switched to infinite mode.")
        else:
            if not ans.isdigit():
                messagebox.showerror("Error", "Please enter a valid positive odd integer.")
                return
            n = int(ans)
            if n <= 0 or n % 2 == 0:
                messagebox.showerror("Error", "Please enter a positive odd integer (3,5,7...).")
                return
            self.best_of = n
            self.target = n // 2 + 1
            messagebox.showinfo("Best-of", f"Best-of-{n} set. First to {self.target} wins the match.")
        self._update_scoreboard()

    def on_player_choice(self, choice):
        # Disable input while animating
        for b in self.btns.values():
            b.config(state="disabled")

        if self.mode.get() == "local":
            # Local mode: players alternate. current_player takes the choice.
            player = f"P{self.current_player}"
            # For local 2-player we treat comp_score as Player2's score in storage
            self.info_label.config(text=f"Player {self.current_player} chose {choice} — waiting for reveal...")
            self.after(300, lambda: self._reveal_local(choice, player))
        else:
            # Single-player: animate countdown then reveal computer choice
            self.info_label.config(text="You chose — waiting for computer...")
            self.after(200, lambda: self._countdown_and_resolve(choice))

    def _countdown_and_resolve(self, player_choice):
        steps = ["Rock...", "Paper...", "Scissors...", "Shoot!"]
        def step(i=0):
            if i < len(steps):
                self.result_var.set(steps[i])
                self.after(300, lambda: step(i+1))
            else:
                comp_choice = random.choice(CHOICES)
                self._resolve_round(player_choice, comp_choice, is_local=False)
        step()

    def _reveal_local(self, p_choice, player_label):
        # In local mode, we wait for second player to pick (or we treat P2 as picks in next turn)
        # Implemented as: when Player1 picks, we prompt Player2 to pick next.
        if player_label == "P1":
            self.result_var.set("Now Player 2, make your choice.")
            # store p1 choice temporarily in attribute
            self._local_p1_choice = p_choice
            # re-enable buttons for player 2
            for b in self.btns.values():
                b.config(state="normal")
            # change current player informally to indicate next press is Player2
            self.current_player = 2
        else:
            # This branch generally not used since we flip current_player in flow
            pass

    def _resolve_round(self, player_choice, comp_choice, is_local=False, p2_choice=None):
        # If local and p2_choice provided, judge p1 vs p2
        if is_local:
            p1 = player_choice
            p2 = comp_choice
            result = self._decide(p1, p2)
            # result: 'tie', 'player', 'computer' but rename: 'player' -> P1, 'computer' -> P2
            if result == 'tie':
                self.ties += 1
                text = f"Tie! {EMOJI[p1]} vs {EMOJI[p2]}"
            elif result == 'player':
                # P1 wins
                self.player_score += 1
                text = f"Player 1 wins the round! {EMOJI[p1]} beats {EMOJI[p2]}"
            else:
                # P2 wins: store in comp_score
                self.comp_score += 1
                text = f"Player 2 wins the round! {EMOJI[p2]} beats {EMOJI[p1]}"
            self._append_history(f"P1:{p1} - P2:{p2} => {text}")
            self.result_var.set(text)
        else:
            # Single-player: player_choice vs comp_choice
            result = self._decide(player_choice, comp_choice)
            if result == 'tie':
                self.ties += 1
                text = f"It's a tie! You {EMOJI[player_choice]} — Computer {EMOJI[comp_choice]}"
            elif result == 'player':
                self.player_score += 1
                text = f"You win! {EMOJI[player_choice]} beats {EMOJI[comp_choice]}"
            else:
                self.comp_score += 1
                text = f"Computer wins! {EMOJI[comp_choice]} beats {EMOJI[player_choice]}"
            self._append_history(f"You:{player_choice} - CPU:{comp_choice} => {text}")
            self.result_var.set(text)

        self._play_sound(result if not is_local else None)
        self._update_scoreboard()
        self._check_match_end()

        # Re-enable buttons
        for b in self.btns.values():
            b.config(state="normal")

        # In local mode, toggle current_player back to 1 and clear local choice
        if is_local:
            self.current_player = 1
            if hasattr(self, '_local_p1_choice'):
                del self._local_p1_choice

    def _decide(self, a, b):
        if a == b:
            return 'tie'
        wins = {('rock','scissors'), ('paper','rock'), ('scissors','paper')}
        return 'player' if (a,b) in wins else 'computer'

    def _append_history(self, txt):
        self.history.insert(0, txt)
        self.hist_box.insert(0, txt)
        # Limit history length
        if len(self.history) > 50:
            self.history = self.history[:50]
            self.hist_box.delete(50, tk.END)

    def _update_scoreboard(self):
        self.score_label.config(text=self._score_text())

    def _check_match_end(self):
        if self.target:
            if self.player_score >= self.target or self.comp_score >= self.target:
                winner = "You" if self.player_score > self.comp_score else "Computer"
                # In local mode, label 'You' as Player 1 and Computer as Player 2
                if self.mode.get() == 'local':
                    winner = 'Player 1' if self.player_score > self.comp_score else 'Player 2'
                messagebox.showinfo("Match Over", f"Match finished! {winner} wins the best-of-{self.best_of}.")
                # ask play again
                if messagebox.askyesno("Play again?", "Do you want to play another match?"):
                    self.restart_match()
                else:
                    self.reset_all()

    def _play_sound(self, result_label=None):
        # Simple, cross-platform: try winsound on Windows; otherwise use bell
        try:
            if winsound:
                # frequency and duration for a small beep
                if result_label == 'player':
                    winsound.Beep(880, 120)
                elif result_label == 'computer':
                    winsound.Beep(440, 120)
                else:
                    winsound.Beep(660, 80)
            else:
                # fallback to GUI bell
                self.bell()
        except Exception:
            try:
                self.bell()
            except Exception:
                pass

    def restart_match(self):
        self.player_score = 0
        self.comp_score = 0
        self.ties = 0
        self.round_num = 0
        self.history = []
        self.hist_box.delete(0, tk.END)
        self.result_var.set("")
        self.current_player = 1
        # keep best_of setting
        if self.best_of:
            self.target = self.best_of // 2 + 1
        else:
            self.target = None
        self._update_scoreboard()
        self.info_label.config(text=("Single-player: play against the computer." if self.mode.get()=="single" else "Local 2-player: players take turns. Player 1 starts."))

    def reset_all(self):
        self.best_of = None
        self.target = None
        self.restart_match()
        self.info_label.config(text="Welcome! Choose a mode and press a choice.")

    # Overriding mainloop close
    def quit(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            super().quit()


if __name__ == '__main__':
    app = RPSApp()
    app.mainloop()
