"""tests/test_project.py - shared test suite.

Owner: Partner B (task B6). Run from the project root:  python -m pytest -q
The slow agent-vs-reference test is skipped unless you pass:  -m slow
"""
import chess
import pytest

from agents import AGENT_REGISTRY
from agents.reference_agent import RandomAgent, ReferenceAgent
from engine.game import get_legal_moves, get_result, is_game_over, make_move, new_game, undo_move
from search.minimax import INF, MATE_SCORE, alphabeta, find_best_move, minimax

# A few positions with tactics in them, used by several tests.
TEST_FENS = [
    chess.STARTING_FEN,
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3",
    "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 4 4",  # Qxf7#
    "8/8/8/4k3/8/8/4P3/4K3 w - - 0 1",
]


def test_legal_moves():
    # TODO(B6): the start position has 20 legal moves; make_move rejects illegal ones.
    raise NotImplementedError("B6: test_legal_moves")


def test_checkmate_detection():
    # TODO(B6): play fool's mate (f3 e5 g4 Qh4#) and check is_game_over / get_result.
    raise NotImplementedError("B6: test_checkmate_detection")


@pytest.mark.parametrize("agent_cls", [ReferenceAgent, *AGENT_REGISTRY.values()])
@pytest.mark.parametrize("fen", TEST_FENS)
def test_alphabeta_equals_minimax(agent_cls, fen):
    # TODO(B6): same score from both searches at depth 2, every agent, every FEN.
    raise NotImplementedError("B6: test_alphabeta_equals_minimax")


def test_finds_mate_in_one():
    # TODO(B6): implement test_finds_mate_in_one.
    raise NotImplementedError("B6: test_finds_mate_in_one")


@pytest.mark.parametrize("name", list(AGENT_REGISTRY))
def test_agent_returns_legal_move(name):
    # TODO(B6): every registered agent returns a legal chess.Move from several positions.
    raise NotImplementedError("B6: test_agent_returns_legal_move")


@pytest.mark.slow
@pytest.mark.parametrize("name", ["Raider (Partner A)", "Fortress (Partner B)"])
def test_agent_beats_random(name):
    # TODO(B6): implement test_agent_beats_random.
    raise NotImplementedError("B6: test_agent_beats_random")
