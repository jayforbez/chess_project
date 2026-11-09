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
    """+1 for White, -1 for Black: multiply a per-colour score by this."""
    return 1 if color == chess.WHITE else -1


def material_score(board):
    """White material minus Black material in centipawns."""
    # TODO(A5): same idea as the reference agent, using PIECE_VALUES.
    raise NotImplementedError("A5: material_score")


def mobility_score(board):
    """Squares attacked by knights, bishops, rooks and queens, excluding squares
    holding our own pieces. Attack-based mobility is a fast stand-in for the
    legal move count and does not depend on whose turn it is."""
    # TODO(A5): for each colour, sum popcount(board.attacks(sq) & ~own_pieces).
    raise NotImplementedError("A5: mobility_score")


def development_score(board):
    """Opening only: reward knights and bishops that have left their home squares,
    and lightly penalise a queen that comes out before the minors."""
    # TODO(A5): skip once fewer than ~10 non-pawn pieces remain (opening is over).
    raise NotImplementedError("A5: development_score")


def king_zone_attack_score(board):
    """Count attacks on the 3x3 zone around each king, weighted by attacker type,
    and convert through SAFETY_TABLE so a pile-up of attackers scores big."""
    # TODO(A5): zone = king square + chess.BB_KING_ATTACKS[king_sq].
    # TODO(A5): for each enemy piece, add weight * popcount(attacks & zone).
    raise NotImplementedError("A5: king_zone_attack_score")


def _bits(mask):
    return chess.SquareSet(mask)


def threat_score(board):
    """Checks, hanging enemy pieces, and general pressure on enemy pieces."""
    # TODO(A5): bonus if the side to move is in check (the other side is giving it).
    # TODO(A5): for each enemy piece we attack: +pressure; if it is undefended, + a share of its value.
    raise NotImplementedError("A5: threat_score")


class RaiderAgent(BaseAgent):
    name = "The Raider"
    author = "Partner A"

    def evaluate(self, board):
        """Sum of the Raider's terms, centipawns from White's point of view."""
        # TODO(A5): add the five terms; apply WEIGHTS['material'] to material_score.
        raise NotImplementedError("A5: evaluate")
