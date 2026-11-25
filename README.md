# Python Chess Agents

A two-agent chess project featuring a custom game engine, Minimax search with Alpha-Beta pruning, a tkinter GUI, and a match harness.

## Team
*   **Partner A (Kemier_`#500001139`):** Built the engine wrapper (`engine/game.py`), the shared search (`search/minimax.py`), the Raider evaluation function (`agents/agent_a_raider.py`), and the match harness (`match/harness.py`).
*   **Partner B (Janae_`#620171986`):** Built the tkinter GUI (`gui/app.py`), the Fortress evaluation function (`agents/agent_b_fortress.py`), the reference agents, and the test suite (`tests/test_project.py`).

## Dependencies
*   Python 3.10+
*   `chess` (python-chess)
*   `pytest`

Install via: `pip install -r requirements.txt`
(Note: Linux users may need `sudo apt install python3-tk` for the GUI).

## How to Run

**1. The GUI (Human vs Agent or Agent vs Agent):**
```bash
python -m gui.app
