# Search: Minimax and Alpha-Beta

## Minimax
The engine uses Minimax to look ahead. White tries to maximize the score, while Black tries to minimize it. 
For a 2-ply search (White moves, Black replies):
1. White looks at every legal move.
2. For each of those, Black looks at every legal reply and evaluates the board.
3. White picks the move where Black's best reply (the minimum score) is as high as possible.
This ensures we never walk into a trap where the opponent gets a massive advantage.

## Alpha-Beta Pruning
Alpha-Beta is an optimization of Minimax. It keeps track of two values:
- **Alpha**: The best score White has found so far.
- **Beta**: The best score Black has found so far.
If we are evaluating a branch and find that it's already worse than a move we've already found elsewhere, we stop searching that branch (a "cutoff"). 
Move ordering makes this prune much faster. By looking at captures, promotions, and checks first (via `order_moves`), we find strong moves early, which raises Alpha and triggers more pruning.

## Node Counts
Here is the node count comparison between pure Minimax and Alpha-Beta at depths 2 and 3 on three different positions:

| FEN | Depth | Minimax nodes | Alpha-Beta nodes | Reduction |
|---|---|---|---|---|
| Starting Position | 2 | 421 | 60 | 85.7% |
| Qxf7# available | 2 | 1275 | 84 | 93.4% |
| Kiwipete | 2 | 2088 | 132 | 93.7% |
| Starting Position | 3 | 9323 | 524 | 94.4% |
| Qxf7# available | 3 | 50422 | 1624 | 96.8% |
| Kiwipete | 3 | 99950 | 2122 | 97.9% |

*Note: Alpha-Beta searches far fewer nodes than Minimax while producing the exact same score, proving the pruning logic is correct. The reduction increases with depth, showing the exponential time saved.*