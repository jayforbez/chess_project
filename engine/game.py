"""engine/game.py - thin wrapper around python-chess.

Owner: Partner A (task A1). Partner B only *uses* these functions.
Every other module talks to the board through this file, so if the
wrapper is right, the GUI, search and harness all agree on the rules.
"""
import chess

# Unicode glyphs: no image files needed for the terminal or the tkinter GUI.
UNICODE_PIECES = {
    "P": "♙", "N": "♘", "B": "♗", "R": "♖", "Q": "♕", "K": "♔",
    "p": "♟", "n": "♞", "b": "♝", "r": "♜", "q": "♛", "k": "♚",
}


def new_game(fen=None):
    """Return a fresh board, or one set up from a FEN string."""
    # TODO(A1): return chess.Board() or chess.Board(fen) when fen is given.
    raise NotImplementedError("A1: new_game")


def get_legal_moves(board):
    """Return the legal moves for the side to move as a list of chess.Move."""
    # TODO(A1): board.legal_moves is a generator; turn it into a list.
    raise NotImplementedError("A1: get_legal_moves")


def make_move(board, move):
    """Play a move on the board. Accepts a chess.Move or a UCI string like 'e2e4'.

    Raises ValueError for an illegal move so GUI bugs show up immediately.
    """
    # TODO(A1): convert a string with chess.Move.from_uci, check legality, push it.
    raise NotImplementedError("A1: make_move")


def undo_move(board):
    """Take back the last move and return it (None if no moves were played)."""
    # TODO(A1): guard against an empty move stack, then board.pop().
    raise NotImplementedError("A1: undo_move")


def is_game_over(board):
    """True on checkmate, stalemate, insufficient material, threefold
    repetition or the 50-move rule (draws are claimed automatically)."""
    # TODO(A1): use board.is_game_over with claim_draw=True.
    raise NotImplementedError("A1: is_game_over")


def get_result(board):
    """Return '1-0', '0-1', '1/2-1/2', or '*' if the game is still going."""
    # TODO(A1): use board.result with claim_draw=True.
    raise NotImplementedError("A1: get_result")


def get_termination(board):
    """Human-readable reason the game ended, e.g. 'CHECKMATE' or 'THREEFOLD_REPETITION'."""
    outcome = board.outcome(claim_draw=True)
    return outcome.termination.name if outcome else "ONGOING"


def board_to_string(board):
    """Board as text with Unicode pieces and rank/file labels (rank 8 on top)."""
    # TODO(A1): loop ranks 7..0 and files 0..7, use board.piece_at(square).
    raise NotImplementedError("A1: board_to_string")
