"""
Position-based ranking configuration
Defines which composite attributes are most relevant for each position type
"""

POSITION_RANKINGS = {
    "CB": {
        "display_name": "Center Backs",
        "key_attributes": [
            "Positioning",
            "Duelling",
            "BoxDefending",
            "DefensiveAction",
            "Composure"
        ]
    },

    "FB/WB": {
        "display_name": "Full Backs / Wing Backs",
        "key_attributes": [
            "Duelling",
            "BallCarrying",
            "ProgPass",
            "Pressing",
            "WidePlay"
        ]
    },

    "DM/CM": {
        "display_name": "Defensive / Central Midfielders",
        "key_attributes": [
            "Positioning",
            "Security",
            "ProgPass",
            "Pressing",
            "DefensiveAction"
        ]
    },

    "AM": {
        "display_name": "Attacking Midfielders",
        "key_attributes": [
            "Creativity",
            "ChanceCreation",
            "BallCarrying",
            "Dribbling",
            "LinkUpPlay"
        ]
    },

    "Winger": {
        "display_name": "Wingers",
        "key_attributes": [
            "Dribbling",
            "WidePlay",
            "Creativity",
            "BallCarrying",
            "LinkUpPlay"
        ]
    },

    "CF": {
        "display_name": "Centre Forwards",
        "key_attributes": [
            "Scoring",
            "AerialThreat",
            "Composure",
            "Pressing",
            "Duelling"
        ]
    },

    "ST": {
        "display_name": "Strikers",
        "key_attributes": [
            "Scoring",
            "AerialThreat",
            "Composure",
            "Pressing",
            "BallCarrying"
        ]
    }
}
