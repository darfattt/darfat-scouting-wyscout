"""
Forward player presets for Player Finder
Defines weighted scoring profiles for different types of attacking players
"""

FORWARD_PRESETS = {
    "Complete Striker": {
        "display_name": "Complete Striker",
        "description": "Traditional number 9 striker: clinical finisher, aerial threat, box presence",
        "components": [
            {"stat": "Non-penalty goals per 90", "weight": 0.25, "use_percentile": False},
            {"stat": "xG per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Goal conversion, %", "weight": 0.20, "use_percentile": False},
            {"stat": "Touches in box per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Shots per 90", "weight": 0.10, "use_percentile": False},
            {"stat": "Aerial duels won, %", "weight": 0.10, "use_percentile": False}
        ],
        "icon": "⚽"
    },
    "Prolific Winger": {
        "display_name": "Prolific Winger",
        "description": "Wide attacker: dribbling, creativity, crossing, chance creation",
        "components": [
            {"stat": "Successful dribbles, %", "weight": 0.25, "use_percentile": False},
            {"stat": "Progressive runs per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Shot assists per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "xA per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Crosses per 90", "weight": 0.10, "use_percentile": False},
            {"stat": "Duels won, %", "weight": 0.10, "use_percentile": False}
        ],
        "icon": "🎯"
    },
    "Attacking Midfielder": {
        "display_name": "Attacking Midfielder",
        "description": "Playmaker: chance creation, passing, vision, linking play",
        "components": [
            {"stat": "Shot assists per 90", "weight": 0.25, "use_percentile": False},
            {"stat": "xA per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Smart passes per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Progressive passes per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Accurate short / medium passes, %", "weight": 0.10, "use_percentile": False},
            {"stat": "Duels won, %", "weight": 0.10, "use_percentile": False}
        ],
        "icon": "⚡"
    },
    "All-Round Forward": {
        "display_name": "All-Round Forward",
        "description": "Versatile attacker: balanced attacking contribution across all areas",
        "components": [
            {"stat": "Non-penalty goals per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Shot assists per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Successful dribbles, %", "weight": 0.15, "use_percentile": False},
            {"stat": "Progressive runs per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "xA per 90", "weight": 0.10, "use_percentile": False},
            {"stat": "Goal conversion, %", "weight": 0.10, "use_percentile": False},
            {"stat": "Duels won, %", "weight": 0.10, "use_percentile": False},
            {"stat": "Passes per 90", "weight": 0.10, "use_percentile": False}
        ],
        "icon": "🌟"
    },
    "Poacher": {
        "display_name": "Poacher",
        "description": "Opportunistic finisher: high conversion rate, box predator",
        "components": [
            {"stat": "Goal conversion, %", "weight": 0.30, "use_percentile": False},
            {"stat": "Non-penalty goals per 90", "weight": 0.25, "use_percentile": False},
            {"stat": "Shots per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Touches in box per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "xG per 90", "weight": 0.10, "use_percentile": False}
        ],
        "icon": "🎯"
    }
}


def get_forward_preset_options():
    """
    Returns list of forward preset names for UI dropdown
    
    Returns:
        List of forward preset names
    """
    return list(FORWARD_PRESETS.keys())


def get_all_preset_options():
    """
    Returns all preset options (defender + forward) for UI dropdown
    
    Returns:
        Dict of all presets merged
    """
    from config.defender_presets import DEFENDER_PRESETS
    
    # Merge defender and forward presets
    all_presets = {}
    all_presets.update(DEFENDER_PRESETS)
    all_presets.update(FORWARD_PRESETS)
    
    return all_presets
