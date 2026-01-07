"""
Position-based ranking configuration
Defines which composite attributes are most relevant for each position type
"""

POSITION_RANKINGS = {
    "DM/CM": {
        "display_name": "Defensive / Central Midfielders",
        "key_attributes": [
            "Tackling",
            "Positioning",
            "Security",
            "ProgPass",
            "Pressing"
        ]
    },

    "CB": {
        "display_name": "Center Backs",
        "key_attributes": [
            "Positioning",
            "Anticipation",
            "Duelling",
            "BoxDefending",
            "Sweeping"
        ]
    },

    "CF": {
        "display_name": "Centre Forwards",
        "key_attributes": [
            "Finishing",
            "AerialThreat",
            "Movement",
            "Composure",
            "Pressing"
        ]
    },

    "Winger": {
        "display_name": "Wingers",
        "key_attributes": [
            "Dribbling",
            "WidePlay",
            "Creativity",
            "ChanceCreation",
            "Movement"
        ]
    },

    "AM": {
        "display_name": "Attacking Midfielders",
        "key_attributes": [
            "Creativity",
            "ChanceCreation",
            "BallCarrying",
            "Composure",
            "ProgPass"
        ]
    },

    "ST": {
        "display_name": "Strikers",
        "key_attributes": [
            "Finishing",
            "Movement",
            "AerialThreat",
            "Composure",
            "Pressing"
        ]
    }
}

