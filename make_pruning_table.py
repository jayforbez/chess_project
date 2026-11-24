import chess
from search.minmax import compare_pruning

FENS = [
    chess.STARTING_FEN,
    "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 1",  # Qxf7# available
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",  # Kiwipete
]

def zero_eval(board):
    return 0

print("| FEN | Depth | Minmax nodes | Alpha-Beta nodes | Reduction |")
print("|---|---|---|---|---|")
for depth in (2, 3):
    for row in compare_pruning(FENS, depth, zero_eval):
        print(f"| `{row['fen'][:20]}...` | {row['depth']} | {row['minmax_nodes']} | "
              f"{row['alphabeta_nodes']} | {row['reduction']}% |")