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
    # Return a fresh board, or one set up from a FEN string.
    if fen:
        return chess.Board()
    return chess.Board()


def get_legal_moves(board):
    # Return the legal moves for the side to move as a list of chess.Move.
    return list(board.legal_moves)

def make_move(board, move):
    # Play a move on the board. Accepts a chess.Move or a UCI string like 'e2e4'.
    # Raises ValueError for an illegal move so GUI bugs show up immediately.

    if isinstance(move, str):
        try:
            move = chess.Move.from_uci(move)
        except ValueError:
            raise ValueError(f"Not a  valid move: {move!r}")
    if move not in board.legal_moves:
        raise ValueError(f"This is an illegal move {move} for {board.fen()}")
    board.push(move)
    return move

def undo_move(board):
    # Take back the last move and return it (None if no moves were played).
    if not board.move_stack:
        return None
    return board.pop()



def is_game_over(board):
    # True on checkmate, stalemate, insufficient material, threefold
    # repetition or the 50-move rule (draws are claimed automatically).
    return  (
        board.is_game_over(claim_draw=False)
        or board.is_repetition(3)
        or board.is_fifty_moves()
    )



def get_result(board):
    # Return '1-0', '0-1', '1/2-1/2', or '*' if the game is still going.
    if not board.is_game_over(claim_draw=False):
        return "*"
    return board.result(claim_draw=False)



def get_termination(board):
    # Human-readable reason the game ended, e.g. 'CHECKMATE' or 'THREEFOLD_REPETITION'.
    outcome = board.outcome(claim_draw=True)
    return outcome.termination.name if outcome else "ONGOING"


def board_to_string(board):
    # Board as text with Unicode pieces and rank/file labels (rank 8 on top).
   return str(board)

