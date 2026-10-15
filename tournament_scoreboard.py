"""Demonstration football league scoreboard for Static Code Analysis Lab 5."""

import re
import secrets
import shutil
import subprocess  # nosec B404
import tempfile
from pathlib import Path

POINTS = {"win": 3, "draw": 1, "loss": 0}
SERVER_PATTERN = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.@-]*$")
teams = {}
matches = []


def add_team(team_name, players=None):
    """Register a team with a fresh player list and zeroed statistics."""
    if players is None:
        players = []
    teams[team_name] = {
        "played": 0,
        "won": 0,
        "drawn": 0,
        "lost": 0,
        "gf": 0,
        "ga": 0,
        "players": list(players),
    }


def match_result(home_goals, away_goals):
    """Return which side won, or draw if the score is level."""
    if home_goals > away_goals:
        return "home"
    if home_goals < away_goals:
        return "away"
    return "draw"


def record_match(home, away, home_goals, away_goals):
    """Record a match and update both teams' statistics."""
    if home not in teams or away not in teams:
        raise KeyError("Both teams must be registered before a match.")
    if home == away:
        raise ValueError("A team cannot play against itself.")
    if home_goals < 0 or away_goals < 0:
        raise ValueError("Goals cannot be negative.")

    result = match_result(home_goals, away_goals)
    sides = ((home, home_goals, away_goals), (away, away_goals, home_goals))
    for team, scored, conceded in sides:
        teams[team]["played"] += 1
        teams[team]["gf"] += scored
        teams[team]["ga"] += conceded

    if result == "draw":
        teams[home]["drawn"] += 1
        teams[away]["drawn"] += 1
    else:
        winner, loser = (home, away) if result == "home" else (away, home)
        teams[winner]["won"] += 1
        teams[loser]["lost"] += 1
    matches.append((home, away, home_goals, away_goals))


def points(team_name):
    """Calculate a team's league points."""
    stats = teams[team_name]
    return stats["won"] * POINTS["win"] + stats["drawn"] * POINTS["draw"]


def goal_difference(team_name):
    """Return goals scored minus goals conceded for a team."""
    return teams[team_name]["gf"] - teams[team_name]["ga"]


def league_table():
    """Return team names sorted by points and goal difference."""
    return sorted(
        teams,
        key=lambda team_name: (points(team_name), goal_difference(team_name)),
        reverse=True,
    )


def is_top_two(team_name):
    """Return whether a team is in the top two.

    Handles tables with fewer than two teams.
    """
    return team_name in league_table()[:2]


def toss_coin():
    """Return a random coin toss result."""
    return secrets.choice(["Heads", "Tails"])


def table_file_path():
    """Create a secure temporary JSON file and return its path."""
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".json",
        prefix="scoreboard_",
        delete=False,
        encoding="utf-8",
    ) as temporary_file:
        return temporary_file.name


def publish_table(server, table_path="table.json"):
    """Publish the table using scp without invoking a shell."""
    if not SERVER_PATTERN.fullmatch(server):
        raise ValueError("Server must be a simple hostname or user@hostname.")
    scp_path = shutil.which("scp")
    if scp_path is None:
        raise RuntimeError(
            "scp was not found. Install an OpenSSH client first."
        )
    table_file = Path(table_path).resolve()
    if not table_file.is_file():
        raise FileNotFoundError(f"Table file does not exist: {table_file}")
    # The executable and argument list are fixed; the host is validated above.
    subprocess.run(  # nosec B603
        [scp_path, str(table_file), f"{server}:/var/www/"],
        check=True,
        timeout=30,
        shell=False,
    )


def main():
    """Run the scoreboard demonstration."""
    teams.clear()
    matches.clear()
    for name in ["Royal Strikers", "City Rovers", "Lake United"]:
        add_team(name)
    add_team("Hill Warriors")
    print("Toss:", toss_coin())
    record_match("Royal Strikers", "City Rovers", 2, 1)
    record_match("Lake United", "Hill Warriors", 0, 0)
    record_match("City Rovers", "Lake United", 3, 2)
    record_match("Hill Warriors", "Royal Strikers", 1, 1)
    print("Pos Team Played Won Drawn Lost Pts")
    for position, name in enumerate(league_table(), 1):
        stats = teams[name]
        print(
            position,
            name,
            stats["played"],
            stats["won"],
            stats["drawn"],
            stats["lost"],
            points(name),
        )
    print("Is City Rovers in the top two?", is_top_two("City Rovers"))
    print("Matches played:", len(matches))


if __name__ == "__main__":
    main()
