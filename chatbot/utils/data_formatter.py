"""
Format data for display and context building
"""
from typing import Dict, List, Any


def format_player_context(player_data: Dict) -> str:
    """
    Format player data for LLM context
    
    Args:
        player_data: Dictionary with player information
    
    Returns:
        Formatted string for prompt
    """
    name = player_data.get('name', 'Unknown')
    age = player_data.get('age', 0)
    team = player_data.get('team', 'Unknown')
    position = player_data.get('position', 'Unknown')
    league = player_data.get('league', 'Unknown')
    
    formatted = f"""
**{name}** ({position}, {age})
Team: {team} | League: {league}

Key Statistics:
"""
    
    stats = player_data.get('stats', {})
    for stat_name, stat_info in stats.items():
        value = stat_info.get('value', 0)
        percentile = stat_info.get('percentile', 50)
        formatted += f"- {stat_name}: {value:.2f} (percentile: {percentile:.1f})\n"
    
    composite_attrs = player_data.get('composite_attrs', {})
    if composite_attrs:
        formatted += "\nComposite Attributes:\n"
        for attr_name, attr_info in composite_attrs.items():
            score = attr_info.get('score', 0)
            display_name = attr_info.get('display_name', attr_name)
            formatted += f"- {display_name}: {score:.1f}\n"
    
    role_matches = player_data.get('role_matches', {})
    if role_matches:
        formatted += "\nRole Fit:\n"
        for role_name, role_info in role_matches.items():
            score = role_info.get('score', 0)
            formatted += f"- {role_name}: {score:.1f}\n"
    
    return formatted


def format_knowledge_context(item: Dict) -> str:
    """
    Format knowledge item for LLM context
    
    Args:
        item: Dictionary with knowledge item info
    
    Returns:
        Formatted string for prompt
    """
    item_type = item.get('type', 'unknown')
    name = item.get('name', 'unknown')
    description = item.get('description', '')
    content = item.get('content', '')
    
    formatted = f"""
## {item_type}: {name}

{description}

{content}
"""
    return formatted


def format_role_context(role: Dict) -> str:
    """
    Format role preset for LLM context
    
    Args:
        role: Dictionary with role preset info
    
    Returns:
        Formatted string for prompt
    """
    name = role.get('display_name', 'Unknown')
    description = role.get('description', '')
    components = role.get('components', [])
    
    formatted = f"""
## Role: {name}

{description}

Components:
"""
    
    for component in components:
        stat = component.get('stat', 'unknown')
        weight = component.get('weight', 0)
        formatted += f"- {stat}: weight={weight:.2f}\n"
    
    return formatted


def extract_top_stats(player_row: Dict, top_n: int = 10) -> List[str]:
    """
    Extract top N stats by percentile from player row
    
    Args:
        player_row: Dictionary with player data including percentile columns
        top_n: Number of top stats to extract
    
    Returns:
        List of stat names
    """
    stats_with_percentiles = []
    
    for key, value in player_row.items():
        if key.endswith('_percentile') and key != 'Player':
            stat_name = key.replace('_percentile', '')
            stats_with_percentiles.append((stat_name, value))
    
    stats_with_percentiles.sort(key=lambda x: x[1], reverse=True)
    
    return [stat[0] for stat in stats_with_percentiles[:top_n]]


def format_players_for_table(players: List[Dict]) -> List[Dict]:
    """
    Format list of players for display in table
    
    Args:
        players: List of player dictionaries
    
    Returns:
        List of formatted player dicts
    """
    formatted = []
    
    for player in players:
        formatted_player = {
            'name': player.get('name', 'Unknown'),
            'team': player.get('team', 'Unknown'),
            'position': player.get('position', 'Unknown'),
            'age': player.get('age', 0),
            'league': player.get('league', 'Unknown')
        }
        formatted.append(formatted_player)
    
    return formatted
