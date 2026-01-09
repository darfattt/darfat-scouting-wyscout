"""
Statistical categories for player comparison
Maps CSV columns to Defensive, Progressive, and Offensive categories
"""

STAT_CATEGORIES = {
    "Defensive": {
        "display_name": "Defensive",
        "stats": [
            {"column": "Duels won, %", "display": "Duels Won %"},
            {"column": "pAdj Tkl+Int per 90", "display": "pAdj Tkl+Int per 90"},
            {"column": "Successful defensive actions per 90", "display": "Defensive Actions per 90"},
            {"column": "PAdj Sliding tackles", "display": "PAdj Sliding Tackles"},
            {"column": "Defensive duels won, %", "display": "Defensive Duels Won %"},
            {"column": "Shots blocked per 90", "display": "Shots Blocked per 90"},
            {"column": "PAdj Interceptions", "display": "PAdj Interceptions"},
            {"column": "Aerial duels won, %", "display": "Aerial Duels Won %"},
            {"column": "Aerial duels won per 90", "display": "Aerial Duels Won per 90"},
        ]
    },
    "Progressive": {
        "display_name": "Progressive",
        "stats": [
            {"column": "Progressive passes per 90", "display": "Progressive Passes per 90"},
            {"column": "Progressive runs per 90", "display": "Progressive Runs per 90"},
            {"column": "Accelerations per 90", "display": "Accelerations per 90"},
            {"column": "Smart passes per 90", "display": "Smart Passes per 90"},
            {"column": "Passes per 90", "display": "Passes per 90"},
            # {"column": "Received Passes", "display": "Received Passes"},
            {"column": "Accurate passes, %", "display": "Pass Accuracy %"},
            {"column": "Accurate short / medium passes, %", "display": "Short/Medium Pass Accuracy %"},
            {"column": "Accurate long passes, %", "display": "Long Pass Accuracy %"},
            {"column": "Crosses per 90", "display": "Crosses per 90"},
            {"column": "Accurate crosses, %", "display": "Accurate Crosses %"},
        ]
    },
    "Offensive": {
        "display_name": "Offensive",
        "stats": [
            {"column": "Non-penalty goals per 90", "display": "Non-penalty Goals per 90"},
            {"column": "npxG per 90", "display": "npxG per 90"},
            {"column": "Assists per 90", "display": "Assists per 90"},
            {"column": "xA per 90", "display": "xA per 90"},
            {"column": "Shot assists per 90", "display": "Shot Assists per 90"},
            {"column": "Second assists per 90", "display": "Second Assists per 90"},
            {"column": "Third assists per 90", "display": "Third Assists per 90"},
            {"column": "Successful dribbles, %", "display": "Successful Dribbles %"},
            {"column": "Goal conversion, %", "display": "Goal Conversion %"},
            {"column": "Touches in box per 90", "display": "Touches in Box per 90"},
            {"column": "Shots per 90", "display": "Shots per 90"},
        ]
    },
    "General": {
        "display_name": "General",
        "stats": [
            {"column": "Fouls per 90", "display": "Fouls per 90"},
            {"column": "Cards per 90", "display": "Cards per 90"},
            {"column": "Fouls suffered per 90", "display": "Fouls Suffered per 90"},
            {"column": "Conceded goals per 90", "display": "Conceded Goals per 90"},
            {"column": "Prevented goals per 90", "display": "Prevented Goals per 90"},
            {"column": "Shots against per 90", "display": "Shots Against per 90"},
            {"column": "Save rate, %", "display": "Save Rate %"},
            {"column": "Exits per 90", "display": "Exits per 90"},
            # {"column": "% of Passes Being Short", "display": "% of Passes Being Short"},
            # {"column": "% of Passes Being Lateral", "display": "% of Passes Being Lateral"},
            {"column": "npxG per shot", "display": "npxG per Shot"},
        ]
    }
}

# Player info columns
PLAYER_INFO_COLUMNS = {
    "name": "Player",
    "age": "Age",
    "team": "Team",
    "country": "Birth country",
    "position": "Position",
    "league": "Competition"
}

# Colors for up to 3 players (matching the reference image)
PLAYER_COLORS = ['#2ecc71', '#3498db', '#e67e22']  # Green, Blue, Orange
