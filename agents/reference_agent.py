"""agents/reference_agent.py - baselines to test against.
"""

import chess

from agents.base_agent import PIECE_VALUES, BaseAgent


class ReferenceAgent(BaseAgent):
    """Material only."""
    name = "Reference"
    author = "Partner B"

    def evaluate(self, board):
        score = 0
        for piece_type, value in PIECE_VALUES.items():
            score += value * len(board.pieces(piece_type, chess.WHITE))
            score -= value * len(board.pieces(piece_type, chess.BLACK))
        return score


