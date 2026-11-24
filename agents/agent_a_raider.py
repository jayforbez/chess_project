"""agents/agent_a_raider.py - Agent A, "The Raider".

Owner: Partner A ONLY. Partner B must not read or edit this file.

Strategy: win by activity and attack. The evaluation rewards piece mobility,
fast development, pressure on the squares around the enemy king, checks and
capture threats. It deliberately ignores pawn structure, so it will accept
doubled or isolated pawns in exchange for the initiative.
"""
import chess

from agents.base_agent import PIECE_VALUES, BaseAgent

# Tune these, and record every change in your design log.
WEIGHTS = {
    "material": 1.0,
    "mobility": 6,           # per square a piece attacks that is not our own piece
    "development": 25,       # per minor piece off its starting square (opening only)
    "early_queen": -10,      # small: the Raider tolerates an early queen sortie
    "king_zone": 1.0,        # multiplier on the attack table below
    "check": 40,             # bonus when the opponent is in check
    "threat": 0.15,          # fraction of an attacked-and-undefended enemy piece's value
    "pressure": 4,           # per attack on any enemy piece
}

# Attack weight per piece type hitting the enemy king zone.
KING_ZONE_ATTACK_WEIGHT = {chess.PAWN: 1, chess.KNIGHT: 2, chess.BISHOP: 2,
                           chess.ROOK: 3, chess.QUEEN: 5, chess.KING: 0}
# Attack units -> centipawns. Non-linear: two attackers are much worse than one.
SAFETY_TABLE = [0, 0, 5, 12, 22, 35, 50, 70, 95, 120, 150, 185, 220, 260, 300,
                340, 380, 420, 460, 500]

MINOR_START = {
    chess.WHITE: {chess.B1, chess.G1, chess.C1, chess.F1},
    chess.BLACK: {chess.B8, chess.G8, chess.C8, chess.F8},
}


def _side(color):
    # +1 for White, -1 for Black: multiply a per-colour score by this.
    return 1 if color == chess.WHITE else -1

def material_score(board):
    # White material minus Black material in centipawns.
    white_mat = sum(len(board.pieces(pt, chess.WHITE)) *val for pt, val in PIECE_VALUES.items())
    black_mat = sum(len(board.pieces(pt, chess.BLACK)) *val for pt, val in PIECE_VALUES.items())
    return white_mat - black_mat

def mobility_score(board):
    # Squares attacked by knights, bishops, rooks and queens, excluding squares
    # holding our own pieces. Attack-based mobility is a fast stand-in for the
    # legal move count and does not depend on whose turn it is."""
    # mobility = 0
    # for pt in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.KING, chess.QUEEN]:
    #     for color in [chess.WHITE, chess.BLACK]:
    #         for sq in board.pieces(pt, color):
    #             mask = board.attacks(sq)
    #             own_pieces = board.occupied_co[color]
    #             mobility += _side(color) * bin(mask & ~own_pieces).count("1")
    #
    # return mobility
        score = 0
        for pt in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for color in [chess.WHITE, chess.BLACK]:
                for sq in board.pieces(pt, color):
                    # Instead of creating a string and counting it, use the mask's bit_count (Python 3.10+)
                    # Or just use python-chess's built-in pop count if bit_count isn't available
                    mask = board.attacks(sq) & ~board.occupied_co[color]
                    score += _side(color) * len(mask)
        return score

def development_score(board):
    # Opening only: reward knights and bishops that have left their home squares,
    # and lightly penalise a queen that comes out before the minors."""
    score = 0
    if board.fullmove_number <= 10 and bin(board.occupied).count("1") <20:
        for color in [chess.WHITE, chess.BLACK]:
            for sq in MINOR_START:
                piece = board.piece_at(sq)
                if piece and piece.color == color:
                    score -= _side(color) * 10

                # penalize early queen moves
                q_sq = board.pieces(chess.QUEEN, color)
                if q_sq:
                    q_sq = list(q_sq)[0]
                    home_q = chess.D1 if color == chess.WHITE else chess.D8

                    if q_sq != home_q:
                        score += _side(color) * WEIGHTS["early_queen"]

    return score


def king_zone_attack_score(board):
    # Count attacks on the 3x3 zone around each king, weighted by attacker type,
    # and convert through SAFETY_TABLE so a pile-up of attackers scores big.
    score = 0
    for color in [chess.WHITE, chess.BLACK]:
        king_sq = board.king(color)
        if king_sq is None:
            continue
        zone_mask = chess.BB_KING_ATTACKS[king_sq] | chess.BB_SQUARES[king_sq]
        attack_unit = 0
        for sq in _bits(zone_mask):
            attackers = board.attackers(not color, sq)
            for a_sq in attackers:
                pt = board.piece_at(a_sq).piece_type
                attack_unit += KING_ZONE_ATTACK_WEIGHT.get(pt, 0)

        safe_unit = min(attack_unit, len(SAFETY_TABLE) -1)
        score += _side(not color) * SAFETY_TABLE[safe_unit]

    return score


def _bits(mask):
    return chess.SquareSet(mask)


def threat_score(board):
    # Checks, hanging enemy pieces, and general pressure on enemy pieces.
    score = 0
    if board.is_check():
        score += _side(board.turn) * WEIGHTS["check"]

    for color in [chess.WHITE, chess.BLACK]:
        opp_color = not color
        for sq in board.pieces(chess.PAWN, opp_color) | board.pieces(chess.KNIGHT, opp_color) | board.pieces(chess.BISHOP, opp_color) | board.pieces(chess.ROOK, opp_color) | board.pieces(chess.QUEEN, opp_color) | board.pieces(chess.KING, opp_color):
            if board.is_attacked_by(color, sq):
                val = PIECE_VALUES.get(board.piece_at(sq).piece_type, 0)
                score += _side(color) * int(val * (WEIGHTS["pressure"] / 100))
                if not board.is_attacked_by(opp_color, sq):
                    score += _side(color) * int(val * (WEIGHTS["threat"]/100))
    return score


class RaiderAgent(BaseAgent):
    def __init__(self, depth=3):
        super().__init__(depth)
        self.name = "Raider Agent"
        self.author = "Partner A"

    def evaluate(self, board):
        # Sum of the Raider's terms, centipawns from White's point of view.
        score = 0
        score += material_score(board) * WEIGHTS["material"]
        score += mobility_score(board) * WEIGHTS["mobility"]
        score += development_score(board)
        score += king_zone_attack_score(board) * WEIGHTS["king_zone"]
        score += threat_score(board)

        return score
