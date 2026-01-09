"""
Statistical categories for player comparison
Maps CSV columns to comprehensive categories for player analysis
"""

STAT_CATEGORIES = {
    "Defensive": {
        "display_name": "Defensive",
        "stats": [
            {"column": "Duels won, %", "display": "Duels Won %"},
            {"column": "Duels per 90", "display": "Duels per 90"},
            {"column": "Defensive duels per 90", "display": "Defensive Duels per 90"},
            {"column": "Defensive duels won, %", "display": "Defensive Duels Won %"},
            {"column": "Aerial duels per 90", "display": "Aerial Duels per 90"},
            {"column": "Aerial duels won, %", "display": "Aerial Duels Won %"},
            {"column": "Sliding tackles per 90", "display": "Sliding Tackles per 90"},
            {"column": "PAdj Sliding tackles", "display": "PAdj Sliding Tackles"},
            {"column": "Shots blocked per 90", "display": "Shots Blocked per 90"},
            {"column": "Interceptions per 90", "display": "Interceptions per 90"},
            {"column": "PAdj Interceptions", "display": "PAdj Interceptions"},
            {"column": "Successful defensive actions per 90", "display": "Defensive Actions per 90"},
            {"column": "Fouls per 90", "display": "Fouls per 90"},
            {"column": "Yellow cards per 90", "display": "Yellow Cards per 90"},
            {"column": "Red cards per 90", "display": "Red Cards per 90"},
            {"column": "Conceded goals per 90", "display": "Conceded Goals per 90"},
            {"column": "Shots against per 90", "display": "Shots Against per 90"},
            {"column": "Prevented goals per 90", "display": "Prevented Goals per 90"},
        ]
    },
    "Offensive": {
        "display_name": "Offensive",
        "stats": [
            {"column": "Goals per 90", "display": "Goals per 90"},
            {"column": "xG per 90", "display": "xG per 90"},
            {"column": "Non-penalty goals per 90", "display": "Non-Penalty Goals per 90"},
            {"column": "Head goals per 90", "display": "Head Goals per 90"},
            {"column": "Shots per 90", "display": "Shots per 90"},
            {"column": "Shots on target, %", "display": "Shots on Target %"},
            {"column": "Goal conversion, %", "display": "Goal Conversion %"},
            {"column": "Assists per 90", "display": "Assists per 90"},
            {"column": "xA per 90", "display": "xA per 90"},
            {"column": "Successful attacking actions per 90", "display": "Attacking Actions per 90"},
            {"column": "Dribbles per 90", "display": "Dribbles per 90"},
            {"column": "Successful dribbles, %", "display": "Successful Dribbles %"},
            {"column": "Offensive duels per 90", "display": "Offensive Duels per 90"},
            {"column": "Offensive duels won, %", "display": "Offensive Duels Won %"},
            {"column": "Touches in box per 90", "display": "Touches in Box per 90"},
            {"column": "Progressive runs per 90", "display": "Progressive Runs per 90"},
            {"column": "Accelerations per 90", "display": "Accelerations per 90"},
            {"column": "Received passes per 90", "display": "Received Passes per 90"},
            {"column": "Received long passes per 90", "display": "Received Long Passes per 90"},
            {"column": "Fouls suffered per 90", "display": "Fouls Suffered per 90"},
            {"column": "Penalties taken", "display": "Penalties Taken"},
            {"column": "Penalty conversion, %", "display": "Penalty Conversion %"},
        ]
    },
    "Progressive": {
        "display_name": "Progressive",
        "stats": [
            {"column": "Passes per 90", "display": "Passes per 90"},
            {"column": "Accurate passes, %", "display": "Pass Accuracy %"},
            {"column": "Forward passes per 90", "display": "Forward Passes per 90"},
            {"column": "Accurate forward passes, %", "display": "Forward Pass Accuracy %"},
            {"column": "Back passes per 90", "display": "Back Passes per 90"},
            {"column": "Accurate back passes, %", "display": "Back Pass Accuracy %"},
            {"column": "Short / medium passes per 90", "display": "Short/Medium Passes per 90"},
            {"column": "Accurate short / medium passes, %", "display": "Short/Medium Pass Accuracy %"},
            {"column": "Long passes per 90", "display": "Long Passes per 90"},
            {"column": "Accurate long passes, %", "display": "Long Pass Accuracy %"},
            {"column": "Progressive passes per 90", "display": "Progressive Passes per 90"},
            {"column": "Accurate progressive passes, %", "display": "Progressive Pass Accuracy %"},
            {"column": "Vertical passes per 90", "display": "Vertical Passes per 90"},
            {"column": "Accurate vertical passes, %", "display": "Vertical Pass Accuracy %"},
            {"column": "Average pass length, m", "display": "Avg Pass Length (m)"},
        ]
    },
    "Chance Creation": {
        "display_name": "Chance Creation",
        "stats": [
            {"column": "Shot assists per 90", "display": "Shot Assists per 90"},
            {"column": "Second assists per 90", "display": "Second Assists per 90"},
            {"column": "Third assists per 90", "display": "Third Assists per 90"},
            {"column": "Smart passes per 90", "display": "Smart Passes per 90"},
            {"column": "Accurate smart passes, %", "display": "Smart Pass Accuracy %"},
            {"column": "Key passes per 90", "display": "Key Passes per 90"},
            {"column": "Passes to final third per 90", "display": "Passes to Final Third per 90"},
            {"column": "Accurate passes to final third, %", "display": "Final Third Pass Accuracy %"},
            {"column": "Passes to penalty area per 90", "display": "Passes to Penalty Area per 90"},
            {"column": "Accurate passes to penalty area, %", "display": "Penalty Area Pass Accuracy %"},
            {"column": "Through passes per 90", "display": "Through Passes per 90"},
            {"column": "Accurate through passes, %", "display": "Through Pass Accuracy %"},
            {"column": "Deep completions per 90", "display": "Deep Completions per 90"},
            {"column": "Deep completed crosses per 90", "display": "Deep Completed Crosses per 90"},
            {"column": "Crosses per 90", "display": "Crosses per 90"},
            {"column": "Accurate crosses, %", "display": "Cross Accuracy %"},
            {"column": "Crosses from left flank per 90", "display": "Left Flank Crosses per 90"},
            {"column": "Accurate crosses from left flank, %", "display": "Left Flank Cross Accuracy %"},
            {"column": "Crosses from right flank per 90", "display": "Right Flank Crosses per 90"},
            {"column": "Accurate crosses from right flank, %", "display": "Right Flank Cross Accuracy %"},
        ]
    },
    "General": {
        "display_name": "General",
        "stats": [
            {"column": "Matches played", "display": "Matches Played"},
            {"column": "Minutes played", "display": "Minutes Played"},
            {"column": "Clean sheets", "display": "Clean Sheets"},
            {"column": "Save rate, %", "display": "Save Rate %"},
            {"column": "xG against per 90", "display": "xG Against per 90"},
            {"column": "Prevented goals per 90", "display": "Prevented Goals per 90"},
            {"column": "Back passes received as GK per 90", "display": "Back Passes Received per 90"},
            {"column": "Exits per 90", "display": "Exits per 90"},
            {"column": "Average long pass length, m", "display": "Avg Long Pass Length (m)"},
            {"column": "Crosses to goalie box per 90", "display": "Crosses to Goalie Box per 90"},
            {"column": "Yellow cards", "display": "Yellow Cards"},
            {"column": "Red cards", "display": "Red Cards"},
        ]
    },
    "Set Pieces": {
        "display_name": "Set Pieces",
        "stats": [
            {"column": "Free kicks per 90", "display": "Free Kicks per 90"},
            {"column": "Direct free kicks per 90", "display": "Direct Free Kicks per 90"},
            {"column": "Direct free kicks on target, %", "display": "Direct Free Kick Accuracy %"},
            {"column": "Corners per 90", "display": "Corners per 90"},
            {"column": "Penalty conversion, %", "display": "Penalty Conversion %"},
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
