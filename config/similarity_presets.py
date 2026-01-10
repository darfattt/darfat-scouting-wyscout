"""
Position and role-based presets for player similarity search
Defines which stats matter most for finding similar players by position/role
"""

from config.defender_presets import DEFENDER_PRESETS
from config.forward_presets import FORWARD_PRESETS
from config.attacking_midfielder_presets import ATTACKING_MIDFIELDER_PRESETS

# ==================== POSITION-BASED PRESETS ====================
# These presets use composite attributes to auto-generate weights
# covering all relevant stats for each position type

POSITION_SIMILARITY_PRESETS = {
    "CB": {
        "display_name": "Center Back (All-round)",
        "description": "Comprehensive stats for center backs focusing on defending, duelling, and progression",
        "applicable_positions": ["CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5"],
        "weights": None,  # Auto-generated from composites
        "composites": ["Security", "Duelling", "BoxDefending", "Sweeping", "ProgPass"]
    },

    "DM/CM": {
        "display_name": "Defensive/Central Midfielder",
        "description": "Comprehensive stats for defensive and central midfielders focusing on ball security, progression, and defensive actions",
        "applicable_positions": ["CDM", "RDM", "LDM", "DMF", "RDMF", "LDMF", "DM"],
        "weights": None,  # Auto-generated from composites
        "composites": ["Security", "ProgPass", "ProactiveDefending", "Duelling", "Sweeping"]
    },

    "FB/WB": {
        "display_name": "Fullback/Wingback",
        "description": "Comprehensive stats for fullbacks and wingbacks focusing on duelling, ball carrying, and progression",
        "applicable_positions": ["LB", "RB", "WB", "RWB", "LWB", "LB5", "RB5", "LWB5", "RWB5"],
        "weights": None,  # Auto-generated from composites
        "composites": ["Duelling", "BallCarrying", "ProgPass", "ProactiveDefending", "Security"]
    },

    "Winger": {
        "display_name": "Winger",
        "description": "Comprehensive stats for wingers focusing on dribbling, creation, and goal threat",
        "applicable_positions": ["LW", "RW", "LWF", "RWF", "RM", "LM"],
        "weights": None,  # Auto-generated from composites
        "composites": ["OneOnOneAbility", "WideCreation", "BallCarrying", "Finishing", "BoxPresence", "Pressing"]
    },

    "AM": {
        "display_name": "Attacking Midfielder",
        "description": "Comprehensive stats for attacking midfielders focusing on creativity, finishing, and build-up play",
        "applicable_positions": ["AMF", "LCMF", "LAMF", "RAMF", "LCMF3", "RCMF3"],
        "weights": None,  # Auto-generated from composites
        "composites": ["FinalBall", "BuildUp", "WideCreation", "Finishing", "Creativity", "Pressing", "BallCarrying"]
    },

    "CF": {
        "display_name": "Centre Forward",
        "description": "Comprehensive stats for centre forwards focusing on finishing, box presence, and link play",
        "applicable_positions": ["CF"],
        "weights": None,  # Auto-generated from composites
        "composites": ["CF_Finishing", "CF_BoxPresence", "CF_Movement", "CF_LinkPlay", "CF_Creativity", "CF_BallCarrying", "CF_Pressing"]
    }
}


# ==================== ROLE-BASED PRESETS ====================
# These presets use weights from existing role definitions
# for specialized player similarity searches

def _extract_weights_from_preset(preset_dict):
    """
    Extract stat weights from preset components

    Args:
        preset_dict: Preset dictionary with 'components' list

    Returns:
        Dict of {stat_name: weight}
    """
    weights = {}
    for component in preset_dict.get("components", []):
        stat = component["stat"]
        weight = component["weight"]
        weights[stat] = weight
    return weights


# Defender role presets
ROLE_SIMILARITY_PRESETS = {
    "Ball_Playing_CB": {
        "display_name": "Ball Playing CB",
        "description": "Excellent passers, able to progress play through thirds and pass over distance",
        "applicable_positions": ["CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5"],
        "source_preset": "DEFENDER_PRESETS.Ball Playing",
        "weights": _extract_weights_from_preset(DEFENDER_PRESETS["Ball Playing"]),
        "icon": "⚡"
    },

    "Libero_CB": {
        "display_name": "Libero",
        "description": "Sweeper style defenders, secure both in and out of possession, cleaning up behind the defensive line",
        "applicable_positions": ["CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5"],
        "source_preset": "DEFENDER_PRESETS.Libero",
        "weights": _extract_weights_from_preset(DEFENDER_PRESETS["Libero"]),
        "icon": "🧹"
    },

    "Wide_Creator_CB": {
        "display_name": "Wide Creator",
        "description": "Creative centre backs in back three, with advanced role and creative responsibility",
        "applicable_positions": ["CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5"],
        "source_preset": "DEFENDER_PRESETS.Wide Creator",
        "weights": _extract_weights_from_preset(DEFENDER_PRESETS["Wide Creator"]),
        "icon": "🎨"
    },

    "Aggressor_CB": {
        "display_name": "Aggressor",
        "description": "Physical aggressive defenders in high line, winning ball in middle third",
        "applicable_positions": ["CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5"],
        "source_preset": "DEFENDER_PRESETS.Aggressor",
        "weights": _extract_weights_from_preset(DEFENDER_PRESETS["Aggressor"]),
        "icon": "⚔️"
    },

    "Physical_Dominator_CB": {
        "display_name": "Physical Dominator",
        "description": "Excellent duelling defenders, using size to control isolated situations",
        "applicable_positions": ["CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5"],
        "source_preset": "DEFENDER_PRESETS.Physical Dominator",
        "weights": _extract_weights_from_preset(DEFENDER_PRESETS["Physical Dominator"]),
        "icon": "💪"
    },

    "Box_Defender_CB": {
        "display_name": "Box Defender",
        "description": "Deep defending centre backs protecting goal and box, blocking and clearing danger",
        "applicable_positions": ["CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5"],
        "source_preset": "DEFENDER_PRESETS.Box Defender",
        "weights": _extract_weights_from_preset(DEFENDER_PRESETS["Box Defender"]),
        "icon": "🧱"
    },

    # Forward role presets
    "Poacher_CF": {
        "display_name": "Poacher",
        "description": "Box specialists, finding space in penalty area to finish",
        "applicable_positions": ["CF"],
        "source_preset": "FORWARD_PRESETS.Poacher",
        "weights": _extract_weights_from_preset(FORWARD_PRESETS["Poacher"]),
        "icon": "🎯"
    },

    "Second_Striker_CF": {
        "display_name": "Second Striker",
        "description": "Work best off main striker, making runs and linking play",
        "applicable_positions": ["CF"],
        "source_preset": "FORWARD_PRESETS.Second Striker",
        "weights": _extract_weights_from_preset(FORWARD_PRESETS["Second Striker"]),
        "icon": "2️⃣"
    },

    "Link_Forward_CF": {
        "display_name": "Link Forward",
        "description": "Offer teammates passing option, hold ball and link play quickly",
        "applicable_positions": ["CF"],
        "source_preset": "FORWARD_PRESETS.Link Forward",
        "weights": _extract_weights_from_preset(FORWARD_PRESETS["Link Forward"]),
        "icon": "🔗"
    },

    "False_Nine_CF": {
        "display_name": "False Nine",
        "description": "Drop off centre backs, creating chances for others with passing",
        "applicable_positions": ["CF"],
        "source_preset": "FORWARD_PRESETS.False Nine",
        "weights": _extract_weights_from_preset(FORWARD_PRESETS["False Nine"]),
        "icon": "🎭"
    },

    "Complete_Forward_CF": {
        "display_name": "Complete Forward",
        "description": "Strong in all areas: movement, goalscoring, creativity, and link play",
        "applicable_positions": ["CF"],
        "source_preset": "FORWARD_PRESETS.Complete Forward",
        "weights": _extract_weights_from_preset(FORWARD_PRESETS["Complete Forward"]),
        "icon": "🌟"
    },

    "Power_Forward_CF": {
        "display_name": "Power Forward",
        "description": "Dynamic, physically powerful, making runs and carrying ball",
        "applicable_positions": ["CF"],
        "source_preset": "FORWARD_PRESETS.Power Forward",
        "weights": _extract_weights_from_preset(FORWARD_PRESETS["Power Forward"]),
        "icon": "💪"
    },

    "Pressing_Forward_CF": {
        "display_name": "Pressing Forward",
        "description": "Selfless forwards expending energy defensively, pressing opponent",
        "applicable_positions": ["CF"],
        "source_preset": "FORWARD_PRESETS.Pressing Forward",
        "weights": _extract_weights_from_preset(FORWARD_PRESETS["Pressing Forward"]),
        "icon": "🔥"
    },

    # Attacking midfielder/winger role presets
    "Winger_AM": {
        "display_name": "Winger",
        "description": "Classic wingers creating chances from wide using dribbling and passing",
        "applicable_positions": ["LW", "RW", "LWF", "RWF", "RM", "LM"],
        "source_preset": "ATTACKING_MIDFIELDER_PRESETS.Winger",
        "weights": _extract_weights_from_preset(ATTACKING_MIDFIELDER_PRESETS["Winger"]),
        "icon": "🎯"
    },

    "Direct_Dribbler_AM": {
        "display_name": "Direct Dribbler",
        "description": "Tricky wingers relentless in 1v1 situations",
        "applicable_positions": ["LW", "RW", "LWF", "RWF", "RM", "LM"],
        "source_preset": "ATTACKING_MIDFIELDER_PRESETS.Direct Dribbler",
        "weights": _extract_weights_from_preset(ATTACKING_MIDFIELDER_PRESETS["Direct Dribbler"]),
        "icon": "🥋"
    },

    "Industrious_Winger_AM": {
        "display_name": "Industrious Winger",
        "description": "Hard working wingers covering ground defensively and offensively",
        "applicable_positions": ["LW", "RW", "LWF", "RWF", "RM", "LM"],
        "source_preset": "ATTACKING_MIDFIELDER_PRESETS.Industrious Winger",
        "weights": _extract_weights_from_preset(ATTACKING_MIDFIELDER_PRESETS["Industrious Winger"]),
        "icon": "🏃"
    },

    "Inside_Forward_AM": {
        "display_name": "Inside Forward",
        "description": "Goal-focused attackers from flank, occupying half space channel",
        "applicable_positions": ["LW", "RW", "LWF", "RWF", "RM", "LM"],
        "source_preset": "ATTACKING_MIDFIELDER_PRESETS.Inside Forward",
        "weights": _extract_weights_from_preset(ATTACKING_MIDFIELDER_PRESETS["Inside Forward"]),
        "icon": "⚽"
    },

    "Shadow_Striker_AM": {
        "display_name": "Shadow Striker",
        "description": "Not ball-dominant, making runs in behind or into box",
        "applicable_positions": ["LW", "RW", "LWF", "RWF", "RM", "LM", "AMF", "LCMF", "LAMF", "RAMF"],
        "source_preset": "ATTACKING_MIDFIELDER_PRESETS.Shadow Striker",
        "weights": _extract_weights_from_preset(ATTACKING_MIDFIELDER_PRESETS["Shadow Striker"]),
        "icon": "👻"
    },

    "Wide_Playmaker_AM": {
        "display_name": "Wide Playmaker",
        "description": "Creative wide men focused on passing and crossing",
        "applicable_positions": ["LW", "RW", "LWF", "RWF", "RM", "LM"],
        "source_preset": "ATTACKING_MIDFIELDER_PRESETS.Wide Playmaker",
        "weights": _extract_weights_from_preset(ATTACKING_MIDFIELDER_PRESETS["Wide Playmaker"]),
        "icon": "🎨"
    },

    "Playmaker_AM": {
        "display_name": "Playmaker",
        "description": "Creative central attacking midfielders, ball-dominant chance creators",
        "applicable_positions": ["AMF", "LCMF", "LAMF", "RAMF", "LCMF3", "RCMF3"],
        "source_preset": "ATTACKING_MIDFIELDER_PRESETS.Playmaker",
        "weights": _extract_weights_from_preset(ATTACKING_MIDFIELDER_PRESETS["Playmaker"]),
        "icon": "⚡"
    }
}


# ==================== HELPER FUNCTIONS ====================

def get_applicable_presets(position: str) -> list:
    """
    Get all applicable presets for a position

    Args:
        position: Specific position (e.g., "CB", "RCB3", "LW")

    Returns:
        List of preset dicts with keys: key, type, display_name, description, applicable_positions
    """
    applicable = []

    # Add position preset
    for preset_key, preset_config in POSITION_SIMILARITY_PRESETS.items():
        if position in preset_config["applicable_positions"]:
            applicable.append({
                "key": preset_key,
                "type": "position",
                **preset_config
            })

    # Add role presets
    for preset_key, preset_config in ROLE_SIMILARITY_PRESETS.items():
        if position in preset_config["applicable_positions"]:
            applicable.append({
                "key": preset_key,
                "type": "role",
                **preset_config
            })

    return applicable


def get_position_preset_keys():
    """
    Get list of all position preset keys

    Returns:
        List of position preset keys
    """
    return list(POSITION_SIMILARITY_PRESETS.keys())


def get_role_preset_keys():
    """
    Get list of all role preset keys

    Returns:
        List of role preset keys
    """
    return list(ROLE_SIMILARITY_PRESETS.keys())
