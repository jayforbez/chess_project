"""match/harness.py - play agents against each other and log everything.

Owner: Partner A (task A6).
Run:  python -m match.harness --games 6 --depth 3
"""
import argparse
import datetime as dt
import json
import os
import time

import chess
import chess.pgn

from engine.game import get_result, get_termination, is_game_over, make_move, new_game

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")


def play_game(white_agent, black_agent, max_plies=300, verbose=False):
    # Play one full game. Returns a dict with result, termination, moves (UCI),
    # san (list of SAN strings), plies, and per-side thinking time / nodes.

    board = new_game()
    game = chess.pgn.Game()
    game.headers["White"] = white_agent.name
    game.headers["Black"] = black_agent.name

    uci_moves = []
    san_moves = []

    # Dicts track stats per color
    times = {chess.WHITE: 0.0, chess.BLACK: 0.0}
    nodes = {chess.WHITE: 0, chess.BLACK: 0}

    node = game
    ply = 0

    while not is_game_over(board) and ply < max_plies:
        color = board.turn
        agent = white_agent if color == chess.WHITE else black_agent

        start_time = time.perf_counter()
        move = agent.choose_move(board)
        times[color] += time.perf_counter() - start_time

        if hasattr(agent, "last_stats"):
            nodes[color] += agent.last_stats.get("nodes", 0)

        san = board.san(move)
        uci_moves.append(move.uci())
        san_moves.append(san)

        if verbose:
            print(f"{ply + 1}. {agent.name}: {san}")

        node = node.add_variation(move)
        make_move(board, move)
        ply += 1

    result = get_result(board)
    termination = get_termination(board)

    # Handles unfinished games
    if ply >= max_plies and not is_game_over(board):
        result = "1/2-1/2"
        termination = "MAX_PLIES"

    game.headers["Result"] = result

    return {
        "white": white_agent.name,
        "black": black_agent.name,
        "result": result,
        "termination": termination,
        "moves": uci_moves,
        "san": san_moves,
        "plies": ply,
        "times": times,
        "nodes": nodes,
        "pgn": str(game)
    }


def log_game(moves, result, white="White", black="Black", extra=None, log_dir=LOG_DIR):
    # Writes the game as PGN (for viewers) and appends a JSON line (for analysis).
    # Returns the PGN path.

    os.makedirs(log_dir, exist_ok=True)

    # Rebuild pgn from moves
    board = new_game()
    game = chess.pgn.Game()
    game.headers["White"] = white
    game.headers["Black"] = black
    game.headers["Result"] = result

    node = game
    for move_str in moves:
        move = chess.Move.from_uci(move_str)
        node = node.add_variation(move)
        board.push(move)

    # Saves pgn file
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    pgn_path = os.path.join(log_dir, f"{timestamp}.pgn")
    with open(pgn_path, "w") as f:
        f.write(str(game))

    # Add to games.jsonl
    jsonl_path = os.path.join(log_dir, f"{timestamp}.jsonl")
    log_entry = {
        "white": white,
        "black": black,
        "result": result,
        "moves": moves,
        "date": timestamp
    }

    if extra:
        log_entry.update(extra)

    with open(jsonl_path, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return pgn_path


def run_match(agent1, agent2, n_games=6, verbose=False):
    # Plays n_games, alternating colours every game. Logs each one.
    # Returns the list of game dicts from play_game.

    results = []
    for i in range(n_games):
        # Swaps colors every games
        if i%2 ==0:
            white_agent, black_agent = agent1, agent2
        else:
            white_agent, black_agent = agent2, agent1

        print(f"Game {i+1}/{n_games}: {white_agent.name} (W) vs {black_agent.name} (B)...", end="", flush=True)

        game_data = play_game(white_agent, black_agent, verbose=verbose)

        # Logs the results
        log_game(
            moves=game_data["moves"],
            result=game_data["result"],
            white=game_data["white"],
            black=game_data["black"],
            extra={
                "termination": game_data["termination"],
                "plies": game_data["plies"],
                "san": game_data["san"],
                "times": game_data["times"],
                "nodes": game_data["nodes"]
            }
        )

        print(f"{game_data['result']} ({game_data['termination']}")
        results.append(game_data)
    return results


def summarize_results(results):
    # Scoreline per agent (win = 1, draw = 0.5) plus W/D/L and average game length.
    scores = {}
    total_plies = 0

    for game in results:
        w = game["white"]
        b = game["black"]
        r = game["result"]

        if w not in scores:
            scores[w] = {"score": 0, "W": 0, "D": 0, "L": 0}
        if b not in scores:
            scores[b] = {"score": 0, "W": 0, "D": 0, "L": 0}

        total_plies += game["plies"]

        if r == "1-0":
            scores[w]["score"] += 1
            scores[w]["W"] += 1
            scores[b]["L"] += 1
        elif r == "0-1":
            scores[b]["score"] += 1
            scores[b]["W"] += 1
            scores[w]["L"] += 1
        else: # 1/2-1/2
            scores[w]["score"] += 0.5
            scores[b]["score"] += 0.5
            scores[w]["D"] += 1
            scores[b]["D"] += 1
    print("\n___Match Summary___")
    for name, stats in scores.items():
        print(f"{name}: {stats['score']} pts (W: {stats['W']}, D: {stats['D']}, L: {stats['L']})")

    if results:
        print(f"Average game length: {total_plies/len(results):.1f} plies")


if __name__ == "__main__":
    from agents import AGENT_REGISTRY

    names = list(AGENT_REGISTRY)
    parser = argparse.ArgumentParser(description="Run an agent-vs-agent match.")
    parser.add_argument("--a", default=names[0], choices=names)
    parser.add_argument("--b", default=names[1], choices=names)
    parser.add_argument("--games", type=int, default=6)
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    a = AGENT_REGISTRY[args.a](depth=args.depth)
    b = AGENT_REGISTRY[args.b](depth=args.depth)
    summarize_results(run_match(a, b, args.games, verbose=args.verbose))
