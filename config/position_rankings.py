"""
Position-based ranking configuration
Defines which composite attributes are most relevant for each position type
"""

POSITION_RANKINGS = {
    "DM/CM": {
        "display_name": "Defensive/Central Midfielders",
        "key_attributes": [
            "Flair",
            "Tackling",
            "Passing",
            "Positioning"
        ]
    },
    "CB": {
        "display_name": "Center Backs",
        "key_attributes": [
            "Positioning",
            "Composure",
            "Passing",
            "Anticipation"
        ]
    }
}
