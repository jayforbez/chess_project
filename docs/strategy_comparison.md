# Strategy Comparison

## The Raider (Casper-a)
The Raider wins by activity and attack. It ignores pawn structure entirely, preferring to accept weak pawns in exchange for the initiative.

Here is how it evaluates the board:
* **Material (1.0):** Standard centipawn values (pawn=100, knight=320, etc.). Keeps the agent grounded so it doesn't throw away pieces.
* **Mobility (6.0):** The Raider values activity highly, giving 6 points for every square attacked by a knight, bishop, rook, or queen. It likes pieces that have long diagonals and open files.
* **Development (25.0):** A flat bonus for moving minor pieces off their starting squares. The Raider wants to attack immediately.
* **Early Queen (-10.0):** A small penalty for bringing the queen out too early, so it doesn't get chased around the board.
* **King Zone (1.0 multiplier):** Uses a `SAFETY_TABLE` to reward piling up attackers (queens, rooks, minors) near the enemy king. The more attackers, the exponentially higher the bonus.
* **Check (40.0):** A flat bonus for giving check. It likes forcing moves.
* **Pressure (4.0):** A small bonus for attacking any enemy piece.
* **Threat (0.15):** If an enemy piece is attacked and completely undefended, the Raider gets 15% of that piece's value.

## The Fortress (Janae)
The Fortress wins by structure. It does not reward mobility or direct attacks, preferring to play quiet, safe moves, build an unbreakable position, and wait for the opponent to overextend.

Here is how it evaluates the board (all values are in centipawns):
* **Material (1.0):** Standard centipawn values, keeping it grounded.
* **Piece-Square Tables (PST) (1.0):** Rewards pieces for being on strong squares (e.g., knights in the center, rooks on open files) and penalizes them for being on the back rank.
* **Doubled Pawns (-20):** Penalizes having two pawns on the same file.
* **Isolated Pawns (-15):** Penalizes pawns with no friendly pawns on adjacent files.
* **Passed Pawns (0 to 100 by rank):** Rewards passed pawns, with the bonus increasing exponentially as the pawn gets closer to promotion (rank 7 is worth 100).
* **Pawn Shield (15):** Rewards having pawns directly in front of the king.
* **Castled (35):** A large bonus for having a castled king. 
* **Castle Rights (10):** A smaller bonus for still being able to castle (if not yet castled).
* **Open King File (-25):** Penalizes the king being on a file with no friendly pawns.
* **Center Control (15 occupy / 5 attack):** Rewards occupying and attacking the four center squares (d4, e4, d5, e5) to ensure the Fortress commands the middle of the board.
