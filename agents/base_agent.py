"""agents/base_agent.py - the common interface. Written together on day 1, then FROZEN.

Every agent (Raider, Fortress, Reference) subclasses BaseAgent and
only overrides evaluate(). The GUI, harness and tests rely on exactly:
    agent.name, agent.depth, agent.evaluate(board) -> int, agent.choose_move(board) -> chess.Move
"""
from abc import ABC, abstractmethod

import chess

from search.minimax import find_best_move, get_node_count, reset_stats

# One shared material scale (centipawns) so scores are comparable across agents.
PIECE_VALUES = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 0,
}


class BaseAgent(ABC):
    name = "BaseAgent"
    author = "?"

    def __init__(self, depth=3):
        self.depth = depth
        self.last_stats = {}

    @abstractmethod
    def evaluate(self, board: chess.Board) -> int:
        """Centipawns from WHITE's point of view. Do not score mate/draw here."""

    def choose_move(self, board: chess.Board) -> chess.Move:
        """Pick a move with the shared alpha-beta search and this agent's evaluate()."""
        reset_stats()
        move, score = find_best_move(board, self.depth, self.evaluate)
        self.last_stats = {"score": score, "nodes": get_node_count(), "depth": self.depth}
        return move

    def __repr__(self):
        return f"{self.name}(depth={self.depth})"
