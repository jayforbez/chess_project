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
        self.canvas.delete("square")
        last = self.board.move_stack[-1] if self.board.move_stack else None
        for sq in chess.SQUARES:
            x, y = chess.square_file(sq) * SQ, (7 - chess.square_rank(sq)) * SQ
            fill = LIGHT if (chess.square_file(sq) + chess.square_rank(sq)) % 2 else DARK
            if last and sq in (last.from_square, last.to_square):
                fill = LAST
            if sq == self.selected:
                fill = SELECT
            self.canvas.create_rectangle(x, y, x + SQ, y + SQ, fill=fill, width=0, tags="square")
            if sq in self.targets:
                r = SQ // 7
                self.canvas.create_oval(x + SQ / 2 - r, y + SQ / 2 - r, x + SQ / 2 + r,
                                        y + SQ / 2 + r, fill=TARGET, width=0, tags="square")

    def draw_pieces(self):
        """Draw every piece as a Unicode glyph centred on its square."""
        self.canvas.delete("piece")
        for sq, piece in self.board.piece_map().items():
            x = chess.square_file(sq) * SQ + SQ / 2
            y = (7 - chess.square_rank(sq)) * SQ + SQ / 2
            self.canvas.create_text(x, y, text=UNICODE_PIECES[piece.symbol()],
                                    font=("DejaVu Sans", int(SQ * 0.62)), fill="#111", tags="piece")

    def square_from_click(self, pos):
        """Convert a click's (x, y) pixel position to a chess square, or None."""
        x, y = pos
        file, rank = int(x // SQ), 7 - int(y // SQ)
        if 0 <= file < 8 and 0 <= rank < 8:
            return chess.square(file, rank)
        return None

    def highlight_moves(self, square):
        """Select `square` and store the destinations of its legal moves."""
        self.selected = square
        self.targets = [m.to_square for m in get_legal_moves(self.board) if m.from_square == square]
        self.redraw()

    def update_status(self, text=None):
        """Show `text`, or a default line: whose turn it is, check, or the result."""
        if text is None:
            if is_game_over(self.board):
                text = f"Game over: {get_result(self.board)} ({get_termination(self.board)})"
            else:
                side = "White" if self.board.turn == chess.WHITE else "Black"
                text = f"{side} to move" + (" - check!" if self.board.is_check() else "")
        self.status.set(text)

    def redraw(self):
        self.draw_board()
        self.draw_pieces()

    # ------------------------------------------------------------------ B2
    def select_agent_menu(self):
        """Side panel: mode, opponent / both agents, depth, colour, buttons."""
        panel = ttk.Frame(self.root, padding=8)
        panel.grid(row=0, column=1, sticky="n")
        names = list(AGENT_REGISTRY)
        self.white_choice = tk.StringVar(value="Human")
        self.black_choice = tk.StringVar(value=names[0])
        self.depth_var = tk.IntVar(value=3)

        ttk.Label(panel, text="White").grid(row=0, column=0, sticky="w")
        ttk.Combobox(panel, textvariable=self.white_choice, values=["Human", *names],
                     state="readonly", width=24).grid(row=1, column=0, pady=(0, 6))
        ttk.Label(panel, text="Black").grid(row=2, column=0, sticky="w")
        ttk.Combobox(panel, textvariable=self.black_choice, values=["Human", *names],
                     state="readonly", width=24).grid(row=3, column=0, pady=(0, 6))
        ttk.Label(panel, text="Search depth").grid(row=4, column=0, sticky="w")
        ttk.Spinbox(panel, from_=1, to=5, textvariable=self.depth_var, width=5).grid(row=5, column=0, sticky="w")

        ttk.Button(panel, text="New game", command=self.new_game_from_menu).grid(row=6, column=0, sticky="ew", pady=(12, 2))
        ttk.Button(panel, text="Undo", command=self.undo).grid(row=7, column=0, sticky="ew", pady=2)
        self.autoplay_btn = ttk.Button(panel, text="Autoplay: off", command=self.toggle_autoplay)
        self.autoplay_btn.grid(row=9, column=0, sticky="ew", pady=2)

    def new_game_from_menu(self):
        """Read the menu and start Human vs Agent or Agent vs Agent."""
        depth = int(self.depth_var.get())
        w, b = self.white_choice.get(), self.black_choice.get()
        make = lambda name: AGENT_REGISTRY[name](depth=depth)
        if w != "Human" and b != "Human":
            self.start_agent_match(make(w), make(b))
            return
        self.mode = "human"
        self.autoplay = False
        self.autoplay_btn.config(text="Autoplay: off")
        self.board = new_game()
        self.selected, self.targets = None, []
        self.agents = {}
        if w != "Human":
            self.agents[chess.WHITE] = make(w)
        if b != "Human":
            self.agents[chess.BLACK] = make(b)
        self.human_color = chess.BLACK if w != "Human" else chess.WHITE
        self.redraw()
        self.update_status()
        self._maybe_agent_turn()

    def handle_human_move(self, click):
        """First click selects one of your pieces, second click moves it."""
        if self.thinking or is_game_over(self.board) or self.board.turn in self.agents:
            return
        sq = self.square_from_click((click.x, click.y))
        if sq is None:
            return
        piece = self.board.piece_at(sq)
        if self.selected is None or (piece and piece.color == self.board.turn):
            if piece and piece.color == self.board.turn:
                self.highlight_moves(sq)
            return
        move = chess.Move(self.selected, sq)
        moving = self.board.piece_at(self.selected)
        if moving.piece_type == chess.PAWN and chess.square_rank(sq) in (0, 7):
            move.promotion = self.handle_promotion()
        self.selected, self.targets = None, []
        if move in self.board.legal_moves:
            make_move(self.board, move)
            self.redraw()
            self.update_status()
            self._maybe_agent_turn()
        else:
            self.redraw()

    def handle_promotion(self):
        """Ask which piece to promote to. Returns a chess piece type (default queen)."""
        choice = {"value": chess.QUEEN}
        win = tk.Toplevel(self.root)
        win.title("Promote to")
        win.transient(self.root)
        glyph = "QRBN" if self.board.turn == chess.WHITE else "qrbn"
        for i, (sym, ptype) in enumerate(zip(glyph, (chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT))):
            def pick(p=ptype):
                choice["value"] = p
                win.destroy()
            tk.Button(win, text=UNICODE_PIECES[sym], font=("DejaVu Sans", 28), command=pick).grid(row=0, column=i)
        win.grab_set()
        self.root.wait_window(win)
        return choice["value"]

    def run_agent_move_threaded(self):
        """Search on a COPY of the board in a worker thread; never touch Tk from it."""
        agent = self.agents[self.board.turn]
        snapshot = self.board.copy()
        fen = self.board.fen()
        self.thinking = True
        self.update_status(f"{agent.name} is thinking (depth {agent.depth})...")

        def work():
            move = agent.choose_move(snapshot)
            self.results.put((fen, move, dict(agent.last_stats)))
        threading.Thread(target=work, daemon=True).start()

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
        self.mode = "agents"
        self.board = new_game()
        self.selected, self.targets = None, []
        self.agents = {chess.WHITE: agent1, chess.BLACK: agent2}
        self.redraw()
        self.update_status(f"{agent1.name} (W) vs {agent2.name} (B): press Step or Autoplay")

    def step_move(self):
        """Play exactly one agent move (agent vs agent mode)."""
        if self.mode != "agents" or self.thinking or is_game_over(self.board):
            if is_game_over(self.board):
                self.autoplay = False
                self.autoplay_btn.config(text="Autoplay: off")
                self.update_status()
            return
        self.run_agent_move_threaded()

    def toggle_autoplay(self):
        """Start or stop automatic stepping."""
        self.autoplay = not self.autoplay
        self.autoplay_btn.config(text=f"Autoplay: {'on' if self.autoplay else 'off'}")
        if self.autoplay:
            self.step_move()

    def set_speed(self, ms):
        """Delay in milliseconds between autoplay moves."""
        self.speed_ms = max(0, int(ms))


def main():
    root = tk.Tk()
    ChessApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
