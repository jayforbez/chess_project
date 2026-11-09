"""agents/reference_agent.py - baselines to test against.

Owner: Partner B (task B5).
"""
import random

import chess

from agents.base_agent import PIECE_VALUES, BaseAgent


class ReferenceAgent(BaseAgent):
    """Material only. If an agent cannot beat this, its extra terms are hurting it."""
    name = "Reference"
    author = "Partner B"

    def evaluate(self, board):
        # TODO(B5): sum PIECE_VALUES for White minus the same for Black.
        raise NotImplementedError("B5: evaluate")


class RandomAgent(BaseAgent):
    """Plays a uniformly random legal move. Useful for smoke tests."""
    name = "Random"
    author = "Partner B"

    def evaluate(self, board):
        return 0

    def choose_move(self, board):
        # TODO(B5): skip the search entirely and pick random.choice of the legal moves.
        raise NotImplementedError("B5: choose_move")
