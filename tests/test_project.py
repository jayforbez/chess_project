"""tests/test_project.py - shared test suite.
"""
import chess
import pytest

from agents import AGENT_REGISTRY
from agents.reference_agent import ReferenceAgent
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
    board = new_game()
    assert len(get_legal_moves(board)) == 20
    make_move(board, "e2e4")
    assert board.piece_at(chess.E4).piece_type == chess.PAWN
    assert undo_move(board).uci() == "e2e4"
    with pytest.raises(ValueError):
        make_move(board, "e2e5")


def test_checkmate_detection():
    board = new_game()
    for uci in ["f2f3", "e7e5", "g2g4", "d8h4"]:
        make_move(board, uci)
    assert is_game_over(board)
    assert get_result(board) == "0-1"


@pytest.mark.parametrize("agent_cls", [ReferenceAgent, *AGENT_REGISTRY.values()])
@pytest.mark.parametrize("fen", TEST_FENS)
def test_alphabeta_equals_minimax(agent_cls, fen):
    agent = agent_cls(depth=2)
    board = chess.Board(fen)
    maximizing = board.turn == chess.WHITE
    mm = minimax(board, 2, maximizing, agent.evaluate)
    ab = alphabeta(board, 2, -INF, INF, maximizing, agent.evaluate)
    assert mm == ab
    assert board.fen() == fen  # the search must leave the board as it found it


def test_finds_mate_in_one():
    board = chess.Board(TEST_FENS[2])
    move, score = find_best_move(board, 2, ReferenceAgent().evaluate)
    assert move == chess.Move.from_uci("h5f7")
    assert score >= MATE_SCORE


@pytest.mark.parametrize("name", list(AGENT_REGISTRY))
def test_agent_returns_legal_move(name):
    agent = AGENT_REGISTRY[name](depth=2)
    for fen in TEST_FENS:
        board = chess.Board(fen)
        move = agent.choose_move(board)
        assert isinstance(move, chess.Move)
        assert move in board.legal_moves
        assert isinstance(agent.evaluate(board), int)


@pytest.mark.slow
@pytest.mark.parametrize("name", ["Raider (Partner A)", "Fortress (Partner B)"])
def test_agent_vs_reference(name):
    """A full game as White against a shallower ReferenceAgent; the agent must not lose."""
    from match.harness import play_game
    agent = AGENT_REGISTRY[name](depth=2)
    game = play_game(agent, ReferenceAgent(depth=1), max_plies=200)
    assert game["result"] in ("1-0", "1/2-1/2")
