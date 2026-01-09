"""
Composite attribute definitions for player analysis
Each attribute is calculated from weighted combinations of statistical metrics
"""

COMPOSITE_ATTRIBUTES = {
    "Positioning": {
        "display_name": "Positioning",
        "description": "Defensive awareness and positioning",
        "components": [
            {"stat": "PAdj Interceptions", "weight": 0.35, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Shots blocked per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Conceded goals per 90", "weight": -0.15, "use_percentile": True},
        ],
        "icon": "🎯"
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
    "Duelling": {
        "display_name": "Duelling",
        "description": "Duel effectively both ground and air, physical dominance",
        "components": [
            {"stat": "Duels won, %", "weight": 0.35, "use_percentile": True},
            {"stat": "Defensive duels won, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Aerial duels won, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Offensive duels won, %", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "💪"
    },
    "BoxDefending": {
        "display_name": "Box Defending",
        "description": "Defend deep in penalty area, clearing danger and blocking shots",
        "components": [
            {"stat": "Shots blocked per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "Aerial duels won, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Conceded goals per 90", "weight": -0.15, "use_percentile": True},
        ],
        "icon": "🧱"
    },
    "Pressing": {
        "display_name": "Pressing",
        "description": "Defensive work rate and pressing intensity",
        "components": [
            {"stat": "Duels won, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Successful defensive actions per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "PAdj Sliding tackles", "weight": 0.20, "use_percentile": True},
            {"stat": "Fouls per 90", "weight": -0.10, "use_percentile": True},
            {"stat": "Progressive runs per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🔥"
    },
    "Composure": {
        "display_name": "Composure",
        "description": "Decision making and technical quality under pressure",
        "components": [
            {"stat": "Accurate short / medium passes, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Goal conversion, %", "weight": 0.20, "use_percentile": True},
            {"stat": "Goals per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "xA per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Shots per 90", "weight": 0.10, "use_percentile": True},
            {"stat": "Fouls per 90", "weight": -0.15, "use_percentile": True},
        ],
        "icon": "🧘"
    },
    "Dribbling": {
        "display_name": "Dribbling",
        "description": "Ball control and 1v1 ability",
        "components": [
            {"stat": "Successful dribbles, %", "weight": 0.30, "use_percentile": True},
            {"stat": "Progressive runs per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Accelerations per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Duels won, %", "weight": 0.15, "use_percentile": True},
            {"stat": "Fouls suffered per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🎯"
    },
    "ChanceCreation": {
        "display_name": "Chance Creation",
        "description": "Playmaking and chance creation ability",
        "components": [
            {"stat": "Shot assists per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "xA per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Smart passes per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Progressive passes per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Second assists per 90", "weight": 0.10, "use_percentile": True},
            {"stat": "Third assists per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🎨"
    },
    "WidePlay": {
        "display_name": "Wide Play",
        "description": "Crossing and wide attacking ability",
        "components": [
            {"stat": "Crosses per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Accurate crosses, %", "weight": 0.20, "use_percentile": True},
            {"stat": "Progressive runs per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Shot assists per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "xA per 90", "weight": 0.10, "use_percentile": True},
            {"stat": "Successful dribbles, %", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🔄"
    },
    "AerialThreat": {
        "display_name": "Aerial Threat",
        "description": "Heading and aerial dominance ability",
        "components": [
            {"stat": "Aerial duels won, %", "weight": 0.40, "use_percentile": True},
            {"stat": "Aerial duels per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Touches in box per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "Goals per 90", "weight": 0.10, "use_percentile": True},
            {"stat": "Head goals per 90", "weight": 0.05, "use_percentile": True},
        ],
        "icon": "🦅"
    },
    "DefensiveAction": {
        "display_name": "Defensive Action",
        "description": "Volume and quality of defensive actions",
        "components": [
            {"stat": "Successful defensive actions per 90", "weight": 0.35, "use_percentile": True},
            {"stat": "Sliding tackles per 90", "weight": 0.20, "use_percentile": True},
            {"stat": "PAdj Sliding tackles", "weight": 0.20, "use_percentile": True},
            {"stat": "PAdj Interceptions", "weight": 0.15, "use_percentile": True},
            {"stat": "Defensive duels won, %", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "⚔️"
    },
    "Scoring": {
        "display_name": "Scoring",
        "description": "Goal-scoring ability and conversion efficiency",
        "components": [
            {"stat": "Goals per 90", "weight": 0.30, "use_percentile": True},
            {"stat": "xG per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Goal conversion, %", "weight": 0.25, "use_percentile": True},
            {"stat": "Shots per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Touches in box per 90", "weight": 0.05, "use_percentile": True},
        ],
        "icon": "⚽"
    },
    "LinkUpPlay": {
        "display_name": "Link Up Play",
        "description": "Connecting midfield and attack through passing and movement",
        "components": [
            {"stat": "Progressive passes per 90", "weight": 0.25, "use_percentile": True},
            {"stat": "Accurate short / medium passes, %", "weight": 0.20, "use_percentile": True},
            {"stat": "Received passes per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Progressive runs per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Key passes per 90", "weight": 0.15, "use_percentile": True},
            {"stat": "Passes to penalty area per 90", "weight": 0.10, "use_percentile": True},
        ],
        "icon": "🔗"
    }
}
