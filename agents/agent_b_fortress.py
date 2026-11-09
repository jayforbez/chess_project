"""agents/agent_b_fortress.py - Agent B, "The Fortress".

Owner: Partner B ONLY. Partner A must not read or edit this file.

Strategy: win by structure. The evaluation rewards good piece placement
(piece-square tables), healthy pawns, a sheltered king and a solid grip on
the centre. It does not reward mobility or attacks directly, so it prefers
quiet, safe moves and lets the opponent overextend.
"""
import chess

from agents.base_agent import PIECE_VALUES, BaseAgent

WEIGHTS = {
    "material": 1.0,
    "pst": 1.0,
    "doubled": -20,          # per extra pawn on a file
    "isolated": -15,         # per pawn with no friendly pawn on an adjacent file
    "passed": [0, 10, 15, 25, 40, 65, 100, 0],  # by rank from that side's view
    "shield": 15,            # per pawn directly in front of the castled king
    "castled": 35,           # king sits on a castled square
    "castle_rights": 10,     # still allowed to castle (not yet castled)
    "open_file_king": -25,   # no friendly pawn on the king's file
    "center_occupy": 15,     # own pawn/piece on d4 e4 d5 e5
    "center_attack": 5,      # per attack on d4 e4 d5 e5
}

# Piece-square tables, written from WHITE's view with rank 8 on the first row.
# For a White piece on square sq use TABLE[chess.square_mirror(sq)];
# for a Black piece use TABLE[sq].
PST = {
    chess.PAWN: [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0],
    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50],
    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20],
    chess.ROOK: [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0],
    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
        0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20],
    chess.KING: [   # middlegame: stay tucked away behind pawns
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20],
}

CENTER = [chess.D4, chess.E4, chess.D5, chess.E5]
CASTLED_SQUARES = {chess.WHITE: {chess.G1, chess.C1, chess.B1, chess.H1},
                   chess.BLACK: {chess.G8, chess.C8, chess.B8, chess.H8}}


def _side(color):
    return 1 if color == chess.WHITE else -1


def material_score(board):
    """White material minus Black material in centipawns."""
    # TODO(B4): use PIECE_VALUES from base_agent.
    raise NotImplementedError("B4: material_score")


def piece_square_score(board):
    """Sum PST bonuses: + for White pieces, - for Black pieces."""
    # TODO(B4): White reads PST[type][chess.square_mirror(sq)], Black reads PST[type][sq].
    raise NotImplementedError("B4: piece_square_score")


def count_doubled(board, color):
    """Extra pawns on files that already have one (3 pawns on a file = 2 doubled)."""
    # TODO(B4): count pawns per file with chess.square_file.
    raise NotImplementedError("B4: count_doubled")


def count_isolated(board, color):
    """Pawns with no friendly pawn on either neighbouring file."""
    # TODO(B4): implement count_isolated.
    raise NotImplementedError("B4: count_isolated")


def passed_pawn_ranks(board, color):
    """Relative rank (0-7, from color's side) of every passed pawn: no enemy pawn
    ahead of it on its own or a neighbouring file."""
    # TODO(B4): for each pawn, look at enemy pawns on files f-1..f+1 further up the board.
    raise NotImplementedError("B4: passed_pawn_ranks")


def count_passed(board, color):
    return len(passed_pawn_ranks(board, color))


def pawn_structure_score(board):
    """Doubled and isolated pawns cost points; passed pawns earn more as they advance."""
    # TODO(B4): implement pawn_structure_score.
    raise NotImplementedError("B4: pawn_structure_score")


def king_safety_score(board):
    """Castled king, pawn shield in front of it, castling rights, no open king file."""
    # TODO(B4): shield = own pawns on the 3 squares one rank in front of the king.
    raise NotImplementedError("B4: king_safety_score")


def center_control_score(board):
    """Occupying and attacking d4, e4, d5, e5."""
    # TODO(B4): implement center_control_score.
    raise NotImplementedError("B4: center_control_score")


class FortressAgent(BaseAgent):
    name = "The Fortress"
    author = "Partner B"

    def evaluate(self, board):
        """Sum of the Fortress's terms, centipawns from White's point of view."""
        # TODO(B4): add the five terms, applying WEIGHTS['material'] and WEIGHTS['pst'].
        raise NotImplementedError("B4: evaluate")
