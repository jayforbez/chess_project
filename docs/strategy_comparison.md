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
