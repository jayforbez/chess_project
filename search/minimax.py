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
import math
import chess

MATE_SCORE = 100_000
DRAW_SCORE = 0
INF = math.inf

# Simple shared node counter. reset_stats() before a search, read after.
STATS = {"nodes": 0}

_MVV_LVA = {chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
            chess.ROOK: 5, chess.QUEEN: 9, chess.KING: 10}


def reset_stats():
    STATS["nodes"] = 0


def get_node_count():
    return STATS["nodes"]


def terminal_score(board, depth):
    # Score a finished position, or return None if the game is not over.
    # The side to move is the side that has been mated. depth is added so a
    # mate found with more depth left (i.e. sooner) scores higher.

   if board.is_checkmate():
       if board.turn == chess.WHITE:
           return -(MATE_SCORE + depth)
       return MATE_SCORE + depth
   if board.is_stalemate() or board.is_insufficient_material() or board.is_repetition(3) or board.is_fifty_moves():
       return DRAW_SCORE
   return None


def minimax(board, depth, maximizing, evaluate_fn):
    # Plain Minimax. Returns the score of `board` searched `depth` plies deep.
    STATS["nodes"] += 1
    score = terminal_score(board, depth)
    if score is not None:
        return score
    if depth == 0:
        return evaluate_fn(board)
    if maximizing:
        best = -INF
        for move in board.legal_moves:
            board.push(move)
            best = max(best, minimax(board, depth - 1, False, evaluate_fn))
            board.pop()
        return best
    else:
        best = INF
        for move in board.legal_moves:
            board.push(move)
            best = min(best, minimax(board, depth - 1, True, evaluate_fn))
            board.pop()
        return best



def order_moves(board):
    # Return legal moves with the most forcing ones first:
    # captures (most valuable victim,  the least valuable attacker), promotions, checks, the rest.
    # Good ordering is what makes Alpha-Beta prune a lot.
    def key(move):
        score = 0
        if board.is_capture(move):
            victim = board.piece_at(move.to_square)
            attacker = board.piece_at(move.from_square)
            victim_val = victim.piece_type if victim else chess.PAWN
            attacker_val = attacker.piece_type if attacker else chess.PAWN
            score += 1000 + 10 * victim_val - attacker_val
        if move.promotion:
            score += 900
        if board.gives_check(move):
            score += 500
        return score
    return sorted(board.legal_moves, key=key, reverse=True)


def alphabeta(board, depth, alpha, beta, maximizing, evaluate_fn):
    # Minimax with Alpha-Beta pruning. Must return the SAME score as
    # minimax(board, depth, maximizing, evaluate_fn) for the same inputs."""
    STATS["nodes"] += 1
    score = terminal_score(board, depth)

    if score is not None:
        return score
    if depth == 0:
        return evaluate_fn(board)

    moves = order_moves(board)
    if maximizing:
        best = -INF
        for move in moves:
            board.push(move)
            best = max(best, alphabeta(board, depth - 1, alpha, beta, False, evaluate_fn))
            board.pop()

            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = INF
        for move in moves:
            board.push(move)
            best = min(best, alphabeta(board, depth - 1, alpha, beta, True, evaluate_fn))
            board.pop()
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def find_best_move(board, depth, evaluate_fn, randomize=True):
    # Search every root move with alphabeta and return (best_move, best_score).
    # With randomize=True a random move is picked among moves with the exact
    # best score, which stops mirror matches from repeating the same game.
    maximizing = board.turn == chess.WHITE
    best_moves = []
    best_score = -INF if maximizing else INF

    for move in order_moves(board):
        board.push(move)
        score = alphabeta(board, depth - 1, -INF, INF, not maximizing, evaluate_fn)
        board.pop()

        if (maximizing and score > best_score) or (not maximizing and score < best_score):
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    if not best_moves:
        return None, best_score
    if randomize:
        return random.choice(best_moves), best_score
    return best_moves[0], best_score


def iterative_deepening(board, max_depth, evaluate_fn, time_limit=None):
    # Optional (A4). Search depth 1, 2, ... max_depth and stop early once
    # time_limit seconds have passed. Returns (move, score, depth_reached).

    start = time.time()
    best_move = None
    best_score = 0
    reached = 0

    for depth in range(1, max_depth + 1):
        if time.time() - start > time_limit:
            break
        move, score = find_best_move(board, depth, evaluate_fn)
        if move is None:
            break
        best_move, best_score, reached = move, score, depth
        if abs(score) >= MATE_SCORE:
            break
    return best_move, best_score, reached


def compare_pruning(fens, depth, evaluate_fn):
    # proof that pruning works: nodes visited by minimax vs alphabeta.
    # Returns a list of rows you can paste into the docs table.
    rows = []
    for fen in fens:
        board = chess.Board(fen)
        maximizing = board.turn == chess.WHITE

        reset_stats()
        s_min = minimax(board, depth, maximizing, evaluate_fn)
        n_min = get_node_count()

        reset_stats()
        s_ab = alphabeta(board, depth, -INF, INF, maximizing, evaluate_fn)
        n_ab = get_node_count()

        assert s_min == s_ab, f"Diverged on {fen}"
        rows.append({
            "fen": fen,
            "depth": depth,
            "minmax_nodes": n_min,
            "alphabeta_nodes": n_ab,
            "reduction": round(100 * (1-n_ab/n_min), 1) if n_min else 0,
        })
    return rows
