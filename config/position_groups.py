"""
Position grouping configuration for simplified filtering
Defines logical position groups for easier player filtering
"""


POSITION_GROUPS = {
    "All": None,
    "CB": ["CB", "RCB", "LCB", "RCB3", "LCB3"],
    "Fullback": ["LB", "RB", "LB5", "RB5", "LWB", "RWB"],
    "Defender": ["CB", "RCB", "LCB", "RCB3", "LCB3", "LB", "RB", "LB5", "RB5", "LWB", "RWB"],
    "DM": ["DMF", "LDMF", "RDMF"],
    "AM": ["AMF", "LAMF", "RAMF"],
    "Central Midfielder": ["DMF", "LDMF", "RDMF", "LCMF", "RCMF", "LCMF3", "RCMF3", "AMF", "LAMF", "RAMF"],
    "Winger": ["LW", "RW", "LWF", "RWF"],
    "Left Winger": ["LW", "LWF"],
    "Right Winger": ["RW", "RWF"],
    "Forward": ["CF", "LW", "RW", "LWF", "RWF", "AMF", "LAMF", "RAMF"],
    "CF": ["CF"]
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
