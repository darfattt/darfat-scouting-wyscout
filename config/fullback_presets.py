"""
Fullback preset definitions for Player Finder
Weighted scoring formulas for different fullback and wingback roles
Focused on modern fullback play styles and responsibilities
"""

FULLBACK_PRESETS = {
    "False Winger": {
        "display_name": "False Winger",
        "description": "A fullback who plays almost as a winger in possession, dribbling and creating in the final third.",
        "archetypes": ["Dilane Bakwa", "Patrick Dorgu", "Keane Lewis-Potter"],
        "components": [
            {"stat": "Touches in final third per 90", "weight": 0.22, "use_percentile": False},
            {"stat": "Crosses per 90", "weight": 0.18, "use_percentile": False},
            {"stat": "Successful dribbles, %", "weight": 0.16, "use_percentile": False},
            {"stat": "Progressive runs per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Key passes per 90", "weight": 0.12, "use_percentile": False},
            {"stat": "Shot assists per 90", "weight": 0.10, "use_percentile": False},
            {"stat": "Passes to penalty area per 90", "weight": 0.07, "use_percentile": False},
        ],
        "icon": "🏃‍♂️"
    },

    "Flyer": {
        "display_name": "Flyer",
        "description": "High energy, box-to-box style fullbacks that press high, overlap well and cover a lot of ground.",
        "archetypes": ["Jeremie Frimpong", "Diego Moreira", "Alessandro Zanoli"],
        "components": [
            {"stat": "Progressive runs per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Touches in final third per 90", "weight": 0.18, "use_percentile": False},
            {"stat": "Successful defensive actions per 90", "weight": 0.16, "use_percentile": False},
            {"stat": "Accelerations per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Defensive duels per 90", "weight": 0.14, "use_percentile": False},
            {"stat": "Crosses per 90", "weight": 0.10, "use_percentile": False},
            {"stat": "Passes to final third per 90", "weight": 0.07, "use_percentile": False},
        ],
        "icon": "🚀"
    },

    "Playmaker": {
        "display_name": "Playmaker",
        "description": "Creative fullbacks who do their offensive work from deep, often inverting or holding a position in the half space, playing a lot of passes to progress and create.",
        "archetypes": ["Maximilian Mittelstädt", "Nuno Mendes", "Przemysław Frankowski"],
        "components": [
            {"stat": "Progressive passes per 90", "weight": 0.25, "use_percentile": False},
            {"stat": "Smart passes per 90", "weight": 0.18, "use_percentile": False},
            {"stat": "Passes to final third per 90", "weight": 0.16, "use_percentile": False},
            {"stat": "xA per 90", "weight": 0.14, "use_percentile": False},
            {"stat": "Key passes per 90", "weight": 0.12, "use_percentile": False},
            {"stat": "Passes per 90", "weight": 0.08, "use_percentile": False},
            {"stat": "Passes to penalty area per 90", "weight": 0.07, "use_percentile": False},
        ],
        "icon": "🎨"
    },

    "Safety": {
        "display_name": "Safety",
        "description": "A player used primarily as a secure passing option, who can help defuse danger as it is created. They often tuck into midfield during possession.",
        "archetypes": ["Carlos Augusto", "Myles Lewis-Skelly", "Raphaël Guerreiro"],
        "components": [
            {"stat": "Accurate short / medium passes, %", "weight": 0.28, "use_percentile": False},
            {"stat": "Accurate passes, %", "weight": 0.20, "use_percentile": False},
            {"stat": "Successful dribbles, %", "weight": 0.18, "use_percentile": False},
            {"stat": "Duels won, %", "weight": 0.15, "use_percentile": False},
            {"stat": "Progressive runs per 90", "weight": 0.12, "use_percentile": False},
            {"stat": "Fouls per 90", "weight": -0.07, "use_percentile": False},
        ],
        "icon": "🛡️"
    },

    "Ball Winner": {
        "display_name": "Ball Winner",
        "description": "Tenacious fullbacks that like to win the ball back with high pressing and duelling.",
        "archetypes": ["Daniel Muñoz", "Ali Abdi", "Nordi Mukiele"],
        "components": [
            {"stat": "Successful defensive actions per 90", "weight": 0.22, "use_percentile": False},
            {"stat": "Defensive duels per 90", "weight": 0.18, "use_percentile": False},
            {"stat": "Duels won, %", "weight": 0.18, "use_percentile": False},
            {"stat": "Defensive duels won, %", "weight": 0.16, "use_percentile": False},
            {"stat": "PAdj Sliding tackles", "weight": 0.12, "use_percentile": False},
            {"stat": "Interceptions per 90", "weight": 0.10, "use_percentile": False},
            {"stat": "Fouls per 90", "weight": -0.06, "use_percentile": False},
        ],
        "icon": "⚔️"
    },

    "Defensive Fullback": {
        "display_name": "Defensive Fullback",
        "description": "Solid defenders, sometimes tucking into a hybrid centre back and fullback role, who offer most value in defending the box.",
        "archetypes": ["Vladimír Coufal", "Ben White", "Neco Williams"],
        "components": [
            {"stat": "Shots blocked per 90", "weight": 0.25, "use_percentile": False},
            {"stat": "Aerial duels won, %", "weight": 0.22, "use_percentile": False},
            {"stat": "Successful defensive actions per 90", "weight": 0.20, "use_percentile": False},
            {"stat": "Interceptions per 90", "weight": 0.15, "use_percentile": False},
            {"stat": "Conceded goals per 90", "weight": -0.12, "use_percentile": False},
            {"stat": "Duels won, %", "weight": 0.06, "use_percentile": False},
        ],
        "icon": "🧱"
    }
}


def get_fullback_preset_options():
    """
    Returns list of fullback preset names for UI dropdown

    Returns:
        List of fullback preset names
    """
    return list(FULLBACK_PRESETS.keys())
