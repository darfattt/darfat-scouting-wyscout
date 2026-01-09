"""
Defender preset definitions for Player Finder
Weighted scoring formulas for different defender profiles
"""

DEFENDER_PRESETS = {
    "Central Defend": {
        "display_name": "Central Defend",
        "description": "Traditional center back focused on aerial dominance and defensive duels",
        "components": [
            {"stat": "Aerial duels won, %", "weight": 0.30, "use_percentile": False},
            {"stat": "Defensive duels won, %", "weight": 0.25, "use_percentile": False},
            {"stat": "Sliding tackles per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Successful defensive actions per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Conceded goals per 90", "weight": -0.10, "use_percentile": False},
        ],
        "icon": "🛡️"
    },
    "Ball Playing Defender": {
        "display_name": "Ball Playing Defender",
        "description": "Modern defender with strong passing and build-up play ability",
        "components": [
            {"stat": "Accurate short / medium passes, %", "weight": 0.30, "use_percentile": False},
            {"stat": "Progressive passes per 90", "weight": 0.25, "use_percentile": False},
            {"stat": "Accurate long passes, %", "weight": 0.20, "use_percentile": False},
            {"stat": "Sliding tackles per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Passes per 90", "weight": 0.10, "use_percentile": False},
        ],
        "icon": "⚡"
    },
    "Build Up Score": {
        "display_name": "Build Up Score",
        "description": "Emphasizes progressive passing and ball progression from defense",
        "components": [
            {"stat": "Progressive passes per 90", "weight": 0.30, "use_percentile": False},
            {"stat": "Passes per 90", "weight": 0.25, "use_percentile": False},
            {"stat": "Accurate short / medium passes, %", "weight": 0.20, "use_percentile": False},
            {"stat": "Progressive runs per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Accelerations per 90", "weight": 0.10, "use_percentile": False},
        ],
        "icon": "🎯"
    },
    "Defensive Score": {
        "display_name": "Defensive Score",
        "description": "Pure defensive actions and engagement",
        "components": [
            {"stat": "Successful defensive actions per 90", "weight": 0.25, "use_percentile": False},
            {"stat": "PAdj Sliding tackles", "weight": 0.25, "use_percentile": False},
            {"stat": "Defensive duels won, %", "weight": 0.20, "use_percentile": False},
            {"stat": "PAdj Interceptions", "weight": 0.15, "use_percentile": False},
            {"stat": "Shots blocked per 90", "weight": 0.15, "use_percentile": False},
        ],
        "icon": "🔒"
    },
    "Wide Center Back": {
        "display_name": "Wide Center Back",
        "description": "Mobile defender suited for wide positions in back 3/5",
        "components": [
            {"stat": "Duels won, %", "weight": 0.25, "use_percentile": False},
            {"stat": "Accelerations per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Progressive runs per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Defensive duels won, %", "weight": 0.15, "use_percentile": False},
            {"stat": "Successful defensive actions per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Fouls per 90", "weight": -0.05, "use_percentile": False},
        ],
        "icon": "🏃"
    }
}
