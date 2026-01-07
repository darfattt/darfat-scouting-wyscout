"""
Composite attribute definitions for player analysis
Each attribute is calculated from weighted combinations of statistical metrics
"""

COMPOSITE_ATTRIBUTES = {
    # "Flair": {
    #     "display_name": "Flair",
    #     "description": "Creative attacking play and dribbling ability",
    #     "components": [
    #         {"stat": "Successful dribbles, %", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Progressive runs per 90", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Smart passes per 90", "weight": 0.20, "use_percentile": True},
    #         {"stat": "Accelerations per 90", "weight": 0.15, "use_percentile": True},
    #         # {"stat": "Received Passes", "weight": 0.15, "use_percentile": True},
    #     ],
    #     "icon": "🎨"
    # },
    "Tackling": {
        "display_name": "Tackling",
        "description": "Defensive engagement and tackling effectiveness",
        "components": [
            {"stat": "Defensive duels won, %", "weight": 0.30, "use_percentile": True},
            {"stat": "pAdj Tkl+Int per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "PAdj Sliding tackles", "weight": 0.10, "use_percentile": True},
            {"stat": "Fouls per 90", "weight": -0.10, "use_percentile": True},
        ],
        "icon": "🛡️"
    },
    # "Passing": {
    #     "display_name": "Passing",
    #     "description": "Overall passing quality and distribution",
    #     "components": [
    #         {"stat": "Accurate short / medium passes, %", "weight": 0.30, "use_percentile": True},
    #         {"stat": "Accurate long passes, %", "weight": 0.20, "use_percentile": True},
    #         {"stat": "Progressive passes per 90", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Passes per 90", "weight": 0.15, "use_percentile": True},
    #         {"stat": "% of Passes Being Short", "weight": 0.10, "use_percentile": True},
    #     ],
    #     "icon": "⚡"
    # },
    "Positioning": {
        "display_name": "Positioning",
        "description": "Defensive awareness and positioning",
        "components": [
            {"stat": "PAdj Interceptions", "weight": 0.30, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Shots blocked per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Conceded goals per 90", "weight": -0.20, "use_percentile": True},
        ],
        "icon": "🎯"
    },
    # "Composure": {
    #     "display_name": "Composure",
    #     "description": "Calmness under pressure and discipline",
    #     "components": [
    #         {"stat": "Accurate short / medium passes, %", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Defensive duels won, %", "weight": 0.25, "use_percentile": True},
    #         {"stat": "Progressive passes per 90", "weight": 0.20, "use_percentile": True},
    #         {"stat": "Fouls per 90", "weight": -0.15, "use_percentile": True},
    #         {"stat": "Cards per 90", "weight": -0.15, "use_percentile": True},
    #     ],
    #     "icon": "🧘"
    # },
    "Anticipation": {
        "display_name": "Anticipation",
        "description": "Reading the game and intercepting danger",
        "components": [
            {"stat": "PAdj Interceptions", "weight": 0.30, "use_percentile": True},
            {"stat": "pAdj Tkl+Int per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Duels won, %", "weight": 0.20, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Fouls per 90", "weight": -0.10, "use_percentile": True},
        ],
        "icon": "👁️"
    },
    "Security": {
        "display_name": "Security",
        "description": "Retain possession under pressure through passing and ball carrying",
        "components": [
            {"stat": "Accurate short / medium passes, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Successful dribbles, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Accurate passes, %", "weight": 0.20, "use_percentile": True},
            {"stat": "Progressive runs per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Fouls per 90", "weight": -0.10, "use_percentile": True},
        ],
        "icon": "🛡️"
    },
    "ProgPass": {
        "display_name": "Prog. Pass",
        "description": "Progress possession through expansive and forward passing",
        "components": [
            {"stat": "Progressive passes per 90", "weight": 0.35, "use_percentile": True},
            {"stat": "Accurate long passes, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Smart passes per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Passes per 90", "weight": 0.15, "use_percentile": True},
        ],
        "icon": "⚡"
    },
    "BallCarrying": {
        "display_name": "Ball Carrying",
        "description": "Dribble and carry the ball up the pitch, exploiting space",
        "components": [
            {"stat": "Progressive runs per 90", "weight": 0.35, "use_percentile": True},
            {"stat": "Successful dribbles, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Accelerations per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Duels won, %", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🏃"
    },
    "Creativity": {
        "display_name": "Creativity",
        "description": "Create chances through passing, penetrating box with passes/crosses",
        "components": [
            {"stat": "Smart passes per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Shot assists per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Crosses per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "xA per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Accurate crosses, %", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🎨"
    },
    "ProactiveDefending": {
        "display_name": "Proactive Defending",
        "description": "Aggressively win ball back, high tackles, pressing",
        "components": [
            {"stat": "pAdj Tkl+Int per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Defensive duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "PAdj Interceptions", "weight": 0.15, "use_percentile": True},
        ],
        "icon": "⚔️"
    },
    "Duelling": {
        "display_name": "Duelling",
        "description": "Duel effectively both ground and air, physical dominance",
        "components": [
            {"stat": "Duels won, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Defensive duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Aerial duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Aerial duels won per 90", "weight": 0.20, "use_percentile": True},
        ],
        "icon": "💪"
    },
    "BoxDefending": {
        "display_name": "Box Defending",
        "description": "Defend deep in penalty area, clearing danger and blocking shots",
        "components": [
            {"stat": "Shots blocked per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Aerial duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Conceded goals per 90", "weight": -0.20, "use_percentile": True},
        ],
        "icon": "🧱"
    },
    "Sweeping": {
        "display_name": "Sweeping",
        "description": "Sweep behind defensive line, clean up danger with tackling",
        "components": [
            {"stat": "PAdj Interceptions", "weight": 0.35, "use_percentile": True},
            {"stat": "pAdj Tkl+Int per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "PAdj Sliding tackles", "weight": 0.20, "use_percentile": True},
            {"stat": "Conceded goals per 90", "weight": -0.15, "use_percentile": True},
        ],
        "icon": "🧹"
    }
}
