"""gui/app.py - tkinter GUI with two modes: Human vs Agent and Agent vs Agent.

Owner: Partner B (tasks B1, B2, B3).
Run:  python -m gui.app

Unicode pieces on a Canvas, so there are no image files to ship.
Agent searches run in a background thread; results come back through a
queue that the Tk main loop polls, so the window never freezes.
"""
import queue
import threading
import tkinter as tk
from tkinter import ttk

import chess

from agents import AGENT_REGISTRY
from engine.game import (UNICODE_PIECES, get_legal_moves, get_result, get_termination,
                         is_game_over, make_move, new_game, undo_move)

SQ = 64                      # pixels per square
LIGHT, DARK = "#EEE6D2", "#8A9A6B"
SELECT, TARGET, LAST = "#E8C547", "#5B8DB8", "#C9B458"


class ChessApp:
    def __init__(self, root):
        self.root = root
        root.title("COMP3220 Chess Agents")
        self.board = new_game()
        self.selected = None          # square the human clicked first
        self.targets = []             # legal destination squares for self.selected
        self.mode = "human"           # "human" or "agents"
        self.human_color = chess.WHITE
        self.agents = {}              # chess.WHITE / chess.BLACK -> agent (agents only)
        self.thinking = False
        self.autoplay = False
        self.speed_ms = 500
        self.results = queue.Queue()

        self.canvas = tk.Canvas(root, width=8 * SQ, height=8 * SQ, highlightthickness=0)
        self.canvas.grid(row=0, column=0, rowspan=2, padx=8, pady=8)
        self.canvas.bind("<Button-1>", self.handle_human_move)
        self.status = tk.StringVar(value="White to move")
        ttk.Label(root, textvariable=self.status, width=48).grid(row=2, column=0, sticky="w", padx=8)
        try:
            self.select_agent_menu()
        except NotImplementedError:
            pass  # lets you test B1 (board drawing) before B2 exists
        self.redraw()
        self.root.after(50, self._poll_results)

    # ------------------------------------------------------------------ B1
    def draw_board(self):
        """Draw the 64 squares plus highlights for the last move, selection and targets."""
        # TODO(B1): rank 8 at the top: row = 7 - rank. Pick the fill from the highlight state.
        raise NotImplementedError("B1: draw_board")

    def draw_pieces(self):
        """Draw every piece as a Unicode glyph centred on its square."""
        # TODO(B1): use UNICODE_PIECES[piece.symbol()] and canvas.create_text.
        raise NotImplementedError("B1: draw_pieces")

    def square_from_click(self, pos):
        """Convert a click's (x, y) pixel position to a chess square, or None."""
        # TODO(B1): file = x // SQ, rank = 7 - y // SQ; check bounds.
        raise NotImplementedError("B1: square_from_click")

    def highlight_moves(self, square):
        """Select `square` and store the destinations of its legal moves."""
        # TODO(B1): implement highlight_moves.
        raise NotImplementedError("B1: highlight_moves")

    def update_status(self, text=None):
        """Show `text`, or a default line: whose turn it is, check, or the result."""
        # TODO(B1): implement update_status.
        raise NotImplementedError("B1: update_status")

    def redraw(self):
        self.draw_board()
        self.draw_pieces()

    # ------------------------------------------------------------------ B2
    def select_agent_menu(self):
        """Side panel: mode, opponent / both agents, depth, colour, buttons."""
        # TODO(B2): Comboboxes filled from AGENT_REGISTRY, a Spinbox for depth.
        raise NotImplementedError("B2: select_agent_menu")

    def new_game_from_menu(self):
        """Read the menu and start Human vs Agent or Agent vs Agent."""
        # TODO(B2): implement new_game_from_menu.
        raise NotImplementedError("B2: new_game_from_menu")

    def handle_human_move(self, click):
        """First click selects one of your pieces, second click moves it."""
        # TODO(B2): ignore clicks while the agent thinks or when it is not a human's turn.
        # TODO(B2): build chess.Move(from, to); ask handle_promotion() for pawn promotions.
        raise NotImplementedError("B2: handle_human_move")

    def handle_promotion(self):
        """Ask which piece to promote to. Returns a chess piece type (default queen)."""
        # TODO(B2): implement handle_promotion.
        raise NotImplementedError("B2: handle_promotion")

    def run_agent_move_threaded(self):
        """Search on a COPY of the board in a worker thread; never touch Tk from it."""
        # TODO(B2): set self.thinking, start a daemon Thread, put (fen, move) on self.results.
        raise NotImplementedError("B2: run_agent_move_threaded")

    def _poll_results(self):
        """Runs on the Tk thread every 50 ms and applies finished agent moves."""
        try:
            fen, move, stats = self.results.get_nowait()
        except queue.Empty:
            pass
        else:
            self.thinking = False
            if fen == self.board.fen() and move is not None:   # ignore stale results
                make_move(self.board, move)
                self.redraw()
                self.update_status()
                if self.mode == "agents":
                    self.status.set(self.status.get() + f"   [{stats.get('nodes')} nodes, eval {stats.get('score')}]")
                    if self.autoplay:
                        self.root.after(self.speed_ms, self.step_move)
                else:
                    self._maybe_agent_turn()
        self.root.after(50, self._poll_results)

    def _maybe_agent_turn(self):
        if not is_game_over(self.board) and self.board.turn in self.agents and not self.thinking:
            self.root.after(150, self.run_agent_move_threaded)

    def undo(self):
        if self.thinking:
            return
        undo_move(self.board)
        if self.mode == "human" and self.agents and self.board.turn in self.agents:
            undo_move(self.board)   # take back the agent's reply too
        self.selected, self.targets = None, []
        self.redraw()
        self.update_status()

    # ------------------------------------------------------------------ B3
    def start_agent_match(self, agent1, agent2):
        """Agent vs agent: agent1 plays White. Use Step or Autoplay to advance."""
        # TODO(B3): implement start_agent_match.
        raise NotImplementedError("B3: start_agent_match")

    def step_move(self):
        """Play exactly one agent move (agent vs agent mode)."""
        # TODO(B3): implement step_move.
        raise NotImplementedError("B3: step_move")

    def toggle_autoplay(self):
        """Start or stop automatic stepping."""
        # TODO(B3): implement toggle_autoplay.
        raise NotImplementedError("B3: toggle_autoplay")

    def set_speed(self, ms):
        """Delay in milliseconds between autoplay moves."""
        # TODO(B3): implement set_speed.
        raise NotImplementedError("B3: set_speed")


def main():
    root = tk.Tk()
    ChessApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
