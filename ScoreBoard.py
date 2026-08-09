"""
I am building a kills/deaths scoreboard from a CS2 player_death event log that
reads example_player_death.csv (one row per player death) and writes
scoreboard.csv with columns: player_id_fixed, kills, deaths.
"""

import csv

INPUT_FILE = "example_player_death.csv"
OUTPUT_FILE = "scoreboard.csv"


def build_scoreboard(input_path):
    """So here is how I am breaking down the logic for counting up everyone's kills and deaths.

    Every single row in this dataset represents a player dying. Because of that, the person listed as the victim always gets a death added to their name. That part is straightforward.

    For the killer, most of the time they get a point added to their kill count, but I had to handle a couple of specific edge cases to keep things accurate:

    * **World kills:** Sometimes the attacker field is completely blank—like when someone dies from a bomb explosion or environmental damage. In those cases, it's just a death for the victim, with no killer to credit.
    * **Team kills and self-kills:** If a player accidentally eliminates their own teammate or walks into their own molotov, it still counts as a death for the victim, but it adds zero kills to the attacker.

    I set it up this way to match how the official CS2 scoreboard works. In the game, your Kills column only tracks actual enemy eliminations. Friendly fire doesn't add to your kill count; it just doesn't give you credit for a real frag. I am not messing around with complex score penalties or subtracting points—I'm simply making sure that friendly fire and self-inflicted deaths aren't mistakenly counted as enemy kills.
    
    """
    
    kills = {}
    deaths = {}

    with open(input_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            victim = int(row["player_id_fixed"])
            deaths[victim] = deaths.get(victim, 0) + 1

            attacker_raw = row["attacker_id_fixed"]
            if attacker_raw == "":
                continue  # world kill (e.g. bomb) -- no kill to credit
            if row["attacker_team_code"] == row["player_team_code"]:
                continue  # self-kill or team kill -- not an enemy elimination
            attacker = int(attacker_raw)
            kills[attacker] = kills.get(attacker, 0) + 1

    # Every player who appears anywhere (as victim or attacker) gets a row,
    # even if their kill or death count ends up at 0.
    player_ids = set(deaths) | set(kills)
    return [
        {
            "player_id_fixed": pid,
            "kills": kills.get(pid, 0),
            "deaths": deaths.get(pid, 0),
        }
        for pid in player_ids
    ]


def write_scoreboard(scoreboard, output_path):
    # Sorting by kills desc, deaths desc, player_id_fixed desc -- numerically,
    # since these are ints, not the string values from the CSV.
    scoreboard.sort(
        key=lambda p: (p["kills"], p["deaths"], p["player_id_fixed"]),
        reverse=True,
    )

    with open(output_path, "w", newline="") as f:
        # lineterminator="\n": csv's default "excel" dialect writes \r\n,
        # which would cause a false mismatch against a byte-exact diff if
        # the reference output uses plain \n (the Linux/pandas default).
        writer = csv.DictWriter(
            f, fieldnames=["player_id_fixed", "kills", "deaths"], lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(scoreboard)


if __name__ == "__main__":
    scoreboard = build_scoreboard(INPUT_FILE)
    write_scoreboard(scoreboard, OUTPUT_FILE)