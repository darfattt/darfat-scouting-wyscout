"""
Position grouping configuration for simplified filtering
Defines logical position groups for easier player filtering
"""

POSITION_GROUPS = {
    "All": None,  # No filtering, all positions
    "CB": ["CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5"],
    "Fullback": ["LB", "RB", "WB", "RWB", "LWB", "LB5", "RB5", "LWB5", "RWB5"],
    "Defender": [
        # CB positions
        "CB", "RCB", "LCB", "RCB3", "LCB3", "CB3", "RCB5", "LCB5",
        # Fullback positions
        "LB", "RB", "WB", "RWB", "LWB", "LB5", "RB5", "LWB5", "RWB5"
    ],
    "DM": ["CDM", "RDM", "LDM", "DMF", "RDMF", "LDMF", "DM"],
    # Forward position groups
    "CF": ["CF"],  # Pure centre forwards
    "Winger": ["LW", "RW", "LWF", "RWF",  "RM",  "LM"],
    "AM": ["AMF", "LCMF", "LAMF", "RAMF","LCMF3", "RCMF3"],
    "Forward": ["CF","LW", "RW", "LWF", "RWF", "AMF", "LCMF", "LAMF", "RAMF",  "RM",  "LM"],
    "Left Winger": ["LW", "LWF", "LM"],
    "Right Winger": ["RW", "RWF", "RM"]
}


def get_position_group_options():
    """
    Returns list of position group names for UI dropdown

    Returns:
        List of position group names
    """
    return list(POSITION_GROUPS.keys())


def filter_by_position_group(df, group_name):
    """
    Filter dataframe by position group

    Args:
        df: Player dataframe
        group_name: Key from POSITION_GROUPS

    Returns:
        Filtered dataframe
    """
    if group_name == "All" or group_name not in POSITION_GROUPS:
        return df.copy()

    positions = POSITION_GROUPS[group_name]
    if positions is None:
        return df.copy()

    # Filter using .isin() for exact matches
    return df[df['Position'].isin(positions)].copy()
