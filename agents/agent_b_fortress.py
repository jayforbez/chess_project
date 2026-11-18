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
    score = 0
    for piece_type, value in PIECE_VALUES.items():
        score += value * (len(board.pieces(piece_type, chess.WHITE))
                          - len(board.pieces(piece_type, chess.BLACK)))
    return score


def piece_square_score(board):
    """Sum PST bonuses: + for White pieces, - for Black pieces."""
    score = 0
    for sq, piece in board.piece_map().items():
        table = PST[piece.piece_type]
        if piece.color == chess.WHITE:
            score += table[chess.square_mirror(sq)]
        else:
            score -= table[sq]
    return score


def count_doubled(board, color):
    """Extra pawns on files that already have one (3 pawns on a file = 2 doubled)."""
    files = [0] * 8
    for sq in board.pieces(chess.PAWN, color):
        files[chess.square_file(sq)] += 1
    return sum(n - 1 for n in files if n > 1)


def count_isolated(board, color):
    """Pawns with no friendly pawn on either neighbouring file."""
    pawn_files = {chess.square_file(sq) for sq in board.pieces(chess.PAWN, color)}
    return sum(1 for sq in board.pieces(chess.PAWN, color)
               if chess.square_file(sq) - 1 not in pawn_files
               and chess.square_file(sq) + 1 not in pawn_files)


def passed_pawn_ranks(board, color):
    """Relative rank (0-7, from color's side) of every passed pawn: no enemy pawn
    ahead of it on its own or a neighbouring file."""
    enemy = board.pieces(chess.PAWN, not color)
    ranks = []
    for sq in board.pieces(chess.PAWN, color):
        f, r = chess.square_file(sq), chess.square_rank(sq)
        blocked = False
        for e in enemy:
            ef, er = chess.square_file(e), chess.square_rank(e)
            if abs(ef - f) <= 1 and ((color == chess.WHITE and er > r) or
                                     (color == chess.BLACK and er < r)):
                blocked = True
                break
        if not blocked:
            ranks.append(r if color == chess.WHITE else 7 - r)
    return ranks


def count_passed(board, color):
    return len(passed_pawn_ranks(board, color))


def pawn_structure_score(board):
    """Doubled and isolated pawns cost points; passed pawns earn more as they advance."""
    score = 0
    for color in (chess.WHITE, chess.BLACK):
        s = (count_doubled(board, color) * WEIGHTS["doubled"]
             + count_isolated(board, color) * WEIGHTS["isolated"]
             + sum(WEIGHTS["passed"][r] for r in passed_pawn_ranks(board, color)))
        score += _side(color) * s
    return score


def king_safety_score(board):
    """Castled king, pawn shield in front of it, castling rights, no open king file."""
    score = 0
    for color in (chess.WHITE, chess.BLACK):
        king_sq = board.king(color)
        if king_sq is None:
            continue
        s = 0
        if king_sq in CASTLED_SQUARES[color]:
            s += WEIGHTS["castled"]
        elif board.has_castling_rights(color):
            s += WEIGHTS["castle_rights"]

        f, r = chess.square_file(king_sq), chess.square_rank(king_sq)
        step = 1 if color == chess.WHITE else -1
        own_pawns = board.pieces(chess.PAWN, color)
        for df in (-1, 0, 1):
            ff, rr = f + df, r + step
            if 0 <= ff <= 7 and 0 <= rr <= 7 and chess.square(ff, rr) in own_pawns:
                s += WEIGHTS["shield"]
        if not any(chess.square_file(p) == f for p in own_pawns):
            s += WEIGHTS["open_file_king"]
        score += _side(color) * s
    return score


def center_control_score(board):
    """Occupying and attacking d4, e4, d5, e5."""
    score = 0
    for color in (chess.WHITE, chess.BLACK):
        s = 0
        for sq in CENTER:
            piece = board.piece_at(sq)
            if piece and piece.color == color:
                s += WEIGHTS["center_occupy"]
            s += len(board.attackers(color, sq)) * WEIGHTS["center_attack"]
        score += _side(color) * s
    return score


class FortressAgent(BaseAgent):
    name = "The Fortress"
    author = "Partner B"

    def evaluate(self, board):
        """Sum of the Fortress's terms, centipawns from White's point of view."""
        return int(
            WEIGHTS["material"] * material_score(board)
            + WEIGHTS["pst"] * piece_square_score(board)
            + pawn_structure_score(board)
            + king_safety_score(board)
            + center_control_score(board)
        )
