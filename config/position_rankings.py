"""
Position-based ranking configuration
Defines which composite attributes are most relevant for each position type
Includes defender, forward, and attacking midfielder positions
"""

POSITION_RANKINGS = {
    # ========== DEFENDER POSITIONS ==========
    
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
    },
    
    # ========== FORWARD POSITIONS ==========
    
    "CF": {
        "display_name": "Centre Forwards",
        "key_attributes": [
            "CF_Finishing",
            "CF_BoxPresence",
            "CF_Movement",
            "CF_LinkPlay",
            "CF_Creativity",
            "CF_BallCarrying",
            "CF_Pressing"
        ]
    },
    
    "Winger": {
        "display_name": "Wingers",
        "key_attributes": [
            "OneOnOneAbility",
            "WideCreation",
            "BallCarrying",
            "Finishing",
            "BoxPresence",
            "Pressing"
        ]
    },
    
    "AM": {
        "display_name": "Attacking Midfielders",
        "key_attributes": [
            "FinalBall",
            "BuildUp",
            "WideCreation",
            "Finishing",
            "Creativity",
            "Pressing",
            "BallCarrying"
        ]
    },
    
    "Complete Forward": {
        "display_name": "Complete Forwards",
        "key_attributes": [
            "CF_Finishing",
            "CF_BoxPresence",
            "CF_Movement",
            "CF_LinkPlay",
            "CF_Creativity",
            "CF_BallCarrying"
        ]
    }
}
