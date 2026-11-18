"""agents/reference_agent.py - baselines to test against.

Owner: Partner B (task B5).
"""

import chess

from agents.base_agent import PIECE_VALUES, BaseAgent


class ReferenceAgent(BaseAgent):
    """Material only. If an agent cannot beat this, its extra terms are hurting it."""
    name = "Reference"
    author = "Partner B"

    def evaluate(self, board):
        score = 0
        for piece_type, value in PIECE_VALUES.items():
            score += value * len(board.pieces(piece_type, chess.WHITE))
            score -= value * len(board.pieces(piece_type, chess.BLACK))
        return score


