"""match/harness.py - play agents against each other and log everything.

Owner: Partner A (task A6).
Run:  python -m match.harness --games 6 --depth 3
"""
import argparse
import datetime as dt
import json
import os
import time

import chess
import chess.pgn

from engine.game import get_result, get_termination, is_game_over, make_move, new_game

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")


def play_game(white_agent, black_agent, max_plies=300, verbose=False):
    """Play one full game. Returns a dict with result, termination, moves (UCI),
    san (list of SAN strings), plies, and per-side thinking time / nodes."""
    # TODO(A6): loop until is_game_over(board) or max_plies;
    # TODO(A6): ask the side to move for choose_move, record SAN before make_move.
    raise NotImplementedError("A6: play_game")


def log_game(moves, result, white="White", black="Black", extra=None, log_dir=LOG_DIR):
    """Write the game as PGN (for viewers) and append a JSON line (for analysis).
    Returns the PGN path."""
    # TODO(A6): rebuild the game with chess.pgn.Game.from_board after pushing the moves.
    raise NotImplementedError("A6: log_game")


def run_match(agent1, agent2, n_games=6, verbose=False):
    """Play n_games, alternating colours every game. Logs each one.
    Returns the list of game dicts from play_game."""
    # TODO(A6): even games -> agent1 is White, odd games -> agent2 is White.
    raise NotImplementedError("A6: run_match")


def summarize_results(results):
    """Scoreline per agent (win = 1, draw = 0.5) plus W/D/L and average game length."""
    # TODO(A6): credit points to results[i]['white'] / ['black'] based on result.
    raise NotImplementedError("A6: summarize_results")


if __name__ == "__main__":
    from agents import AGENT_REGISTRY

    names = list(AGENT_REGISTRY)
    parser = argparse.ArgumentParser(description="Run an agent-vs-agent match.")
    parser.add_argument("--a", default=names[0], choices=names)
    parser.add_argument("--b", default=names[1], choices=names)
    parser.add_argument("--games", type=int, default=6)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    a = AGENT_REGISTRY[args.a](depth=args.depth)
    b = AGENT_REGISTRY[args.b](depth=args.depth)
    summarize_results(run_match(a, b, args.games, verbose=args.verbose))
