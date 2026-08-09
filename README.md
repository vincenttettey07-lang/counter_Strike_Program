# PureSkill.gg Scoreboard Exercise

## What this does
Reads `example_player_death.csv` (one CS2 match's `player_death` event
log) and writes `scoreboard.csv` with three columns — `player_id_fixed`,
`kills`, `deaths` — sorted by kills descending, then deaths descending,
then player_id_fixed descending (numeric sort).

## How to run
Assumes `example_player_death.csv`, `scoreboard.py`, and the interpreter
running it are all in the same directory. Requires only the Python
standard library (`csv`), no external dependencies.

## Logic
- **deaths**: every row counts as one death for `player_id_fixed`.
- **kills**: counts as a kill for `attacker_id_fixed`, except:
  - blank `attacker_id_fixed` (e.g. bomb detonation) -- no one to credit.
  - `attacker_team_code == player_team_code` (a team kill or self-kill)
    -- this matches the official in-game Kills (K) column, which only
    tracks enemy eliminations. Team/self kills add 0 to kills; they are
    not penalized (no -1), since the assignment doesn't ask for a
    separate Score stat.


## Files
- `scoreboard.py` -- the submission script.
- `scoreboard.csv` -- output from running the script against the
  provided `example_player_death.csv`.
- `scoreboard_exploration.ipynb` (optional) -- notebook showing the
  data exploration and reasoning behind the edge-case handling.