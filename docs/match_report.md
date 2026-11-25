# Match report: The Raider vs The Fortress

## Setup
- Games: 6, colours alternated (`python -m match.harness --a Raider --b Fortress --games 6 --depth 3`)
- Search depth: 3, Alpha-Beta with move ordering, random choice among equal best moves
- Draw rules: threefold repetition and the 50-move rule are claimed automatically

## Scoreline
| Agent | Points | W | D | L |
|---|---|---|---|---|
| The Raider (Kemier) | 3.5 | 3 | 1 | 2 |
| The Fortress (Janae) | 2.5 | 2 | 1 | 3 |

## Games
| # | White | Black | Result | Ended by | Plies |
|---|---|---|---|---|---|
| 1 | Raider | Fortress | 0-1 | CHECKMATE | 114 |
| 2 | Fortress | Raider | 0-1 | CHECKMATE | 89 |
| 3 | Raider | Fortress | 1-0 | CHECKMATE | 145 |
| 4 | Fortress | Raider | 1/2-1/2 | MAX_PLIES | 300 |
| 5 | Raider | Fortress | 1-0 | CHECKMATE | 120 |
| 6 | Fortress | Raider | 1-0 | CHECKMATE | 170 |


## Against the reference agent
| Agent | vs Reference (W-D-L) |
|---|----------------------|
| The Raider | 2-0-0                |
| The Fortress | 2-0-0                |


## Interesting moments
### Game 2, move 89 (Checkmate)
The Fortress (White) tried to build a solid pawn structure, but the Raider (Black) sacrificed a pawn for advantage. By move 89, the Raider's queen and rook had infiltrated the Fortress's back rank, leading to a forced checkmate. The Raider's high mobility weight (6.0) allowed it to find the attacking continuation, while the Fortress's material advantage was useless because its pieces were trapped.

## Why the results happened
The evaluation terms explain the close 3.5 - 2.5 scoreline perfectly. 
The Raider's aggressive terms (**Mobility** and **King Zone Attack**) allowed it to win 3 games by checkmate.
However, the Fortress's defensive terms (**Pawn Structure** and **King Safety**) kept it in the match. It won 2 games by punishing the Raider's weak pawns in the endgame, and forced one draw (MAX_PLIES). The Fortress proved that solid structure can survive early aggression, but the Raider's aggressive strategy gave it the slight edge.
