"""
Position-based ranking configuration for defenders
Defines which composite attributes are most relevant for each defender position type
"""

POSITION_RANKINGS = {
    "CB": {
        "display_name": "Center Backs",
        "key_attributes": [
            "Security",
            "Duelling",
            "BoxDefending",
            "Sweeping",
            "ProgPass"
        ]
    },

    "FB/WB": {
        "display_name": "Full Backs / Wing Backs",
        "key_attributes": [
            "Duelling",
            "BallCarrying",
            "ProgPass",
            "ProactiveDefending",
            "Security"
        ]
    },

    "DM/CM": {
        "display_name": "Defensive / Central Midfielders",
        "key_attributes": [
            "Security",
            "ProgPass",
            "ProactiveDefending",
            "Duelling",
            "Sweeping"
        ]
    },

    "Wide CB": {
        "display_name": "Wide Centre Backs",
        "key_attributes": [
            "BallCarrying",
            "Creativity",
            "ProgPass",
            "Duelling",
            "ProactiveDefending"
        ]
    },

    "Back Three": {
        "display_name": "Back Three Defenders",
        "key_attributes": [
            "Security",
            "Sweeping",
            "BoxDefending",
            "Creativity",
            "BallCarrying"
        ]
    }
}
