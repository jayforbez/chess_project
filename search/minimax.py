"""search/minimax.py - shared Minimax + Alpha-Beta search.

Owner: Partner A (tasks A2, A3, A4). Both agents use it.

Contract:
  * evaluate_fn(board) -> int, centipawns, ALWAYS from White's point of view.
  * White is the maximizing player, Black is the minimizing player.
  * Terminal positions are scored HERE, not in the evaluation functions:
      checkmate -> +/-MATE_SCORE (plus remaining depth, so faster mates win)
      draw      -> DRAW_SCORE (0)
"""
import random
import time

import chess

MATE_SCORE = 100_000
DRAW_SCORE = 0
INF = 10**9

# Simple shared node counter. reset_stats() before a search, read after.
STATS = {"nodes": 0}

_MVV_LVA = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 10}


def reset_stats():
    STATS["nodes"] = 0


def get_node_count():
    return STATS["nodes"]


def terminal_score(board, depth):
    """Score a finished position, or return None if the game is not over.

    The side to move is the side that has been mated. depth is added so a
    mate found with more depth left (i.e. sooner) scores higher.
    """
    # TODO(A2): checkmate -> -(MATE_SCORE + depth) if White is mated, +(...) if Black is.
    # TODO(A2): stalemate / insufficient material / 75-move / fivefold -> DRAW_SCORE.
    raise NotImplementedError("A2: terminal_score")


def minimax(board, depth, maximizing, evaluate_fn):
    """Plain Minimax. Returns the score of `board` searched `depth` plies deep."""
    # TODO(A2): count the node in STATS, handle terminal / depth 0,
    # TODO(A2): then push each legal move, recurse with not maximizing, pop.
    raise NotImplementedError("A2: minimax")


def order_moves(board):
    """Return legal moves with the most forcing ones first:
    captures (most valuable victim, least valuable attacker), promotions, checks, the rest.
    Good ordering is what makes Alpha-Beta prune a lot."""
    # TODO(A3): give each move a sort key and return sorted(..., reverse=True).
    raise NotImplementedError("A3: order_moves")


def alphabeta(board, depth, alpha, beta, maximizing, evaluate_fn):
    """Minimax with Alpha-Beta pruning. Must return the SAME score as
    minimax(board, depth, maximizing, evaluate_fn) for the same inputs."""
    # TODO(A3): same shape as minimax, but use order_moves(board),
    # TODO(A3): raise alpha (max) / lower beta (min), and break when alpha >= beta.
    raise NotImplementedError("A3: alphabeta")


def find_best_move(board, depth, evaluate_fn, randomize=True):
    """Search every root move with alphabeta and return (best_move, best_score).

    With randomize=True a random move is picked among moves with the exact
    best score, which stops mirror matches from repeating the same game.
    """
    # TODO(A3): loop over order_moves(board), score each child with alphabeta,
    # TODO(A3): keep the best for the side to move (max for White, min for Black).
    raise NotImplementedError("A3: find_best_move")


def iterative_deepening(board, max_depth, evaluate_fn, time_limit=None):
    """Optional (A4). Search depth 1, 2, ... max_depth and stop early once
    time_limit seconds have passed. Returns (move, score, depth_reached)."""
    # TODO(A4): implement iterative_deepening.
    raise NotImplementedError("A4: iterative_deepening")


def compare_pruning(fens, depth, evaluate_fn):
    """A4 proof that pruning works: nodes visited by minimax vs alphabeta.
    Returns a list of rows you can paste into the docs table."""
    # TODO(A4): implement compare_pruning.
    raise NotImplementedError("A4: compare_pruning")
