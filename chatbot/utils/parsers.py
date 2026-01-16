"""
Parse positions, stats, ages from queries
"""
import re
from typing import Optional, List, Tuple


def parse_position(query: str) -> Optional[str]:
    """
    Extract position from query
    
    Args:
        query: User query string
    
    Returns:
        Position code or None
    """
    positions = [
        'CB', 'DM', 'CM', 'CDM', 'AM', 'CAM', 'CF', 'LW', 'RW',
        'LB', 'RB', 'LWB', 'RWB', 'GK', 'LCB', 'RCB', 'DMF',
        'CMF', 'LMF', 'RMF', 'AMF', 'CF', 'SS', 'LF', 'RF'
    ]
    
    query_lower = query.lower()
    
    for pos in positions:
        if pos.lower() in query_lower:
            return pos
    
    return None


def parse_age_range(query: str) -> Optional[Tuple[int, int]]:
    """
    Extract age range from query
    
    Args:
        query: User query string
    
    Returns:
        Tuple (min_age, max_age) or None
    """
    match = re.search(r'between\s+(\d+)\s+and\s+(\d+)', query.lower())
    if match:
        return (int(match.group(1)), int(match.group(2)))
    
    match = re.search(r'under\s+(\d+)', query.lower())
    if match:
        return (None, int(match.group(1)))
    
    match = re.search(r'over\s+(\d+)', query.lower())
    if match:
        return (int(match.group(1)), None)
    
    return None


def parse_composite_attribute(query: str) -> Optional[str]:
    """
    Extract composite attribute name from query
    
    Args:
        query: User query string
    
    Returns:
        Composite attribute name or None
    """
    attrs = [
        'Security', 'ProgPass', 'BallCarrying', 'Creativity',
        'Finishing', 'BoxPresence', 'Movement', 'Pressing',
        'OneOnOneAbility', 'WideCreation', 'BuildUp', 'FinalBall',
        'DM_Destroying', 'DM_BallWinning', 'DM_Dictating',
        'DM_ProgPass', 'DM_BallCarrying', 'DM_BoxCrashing'
    ]
    
    query_lower = query.lower()
    
    for attr in attrs:
        if attr.lower() in query_lower:
            return attr
    
    return None


def parse_metrics(query: str) -> List[str]:
    """
    Extract metric names from query
    
    Args:
        query: User query string
    
    Returns:
        List of metric names found
    """
    metrics = [
        'xG per 90', 'Goals per 90', 'Assists per 90',
        'Passes per 90', 'Duels won, %', 'Progressive passes per 90',
        'xA per 90', 'Successful dribbles, %', 'Touches in box per 90'
    ]
    
    found = []
    query_lower = query.lower()
    
    for metric in metrics:
        if metric.lower() in query_lower:
            found.append(metric)
    
    return found


def parse_threshold(query: str) -> Optional[float]:
    """
    Extract numerical threshold from query
    
    Args:
        query: User query string
    
    Returns:
        Threshold value or None
    """
    match = re.search(r'[><]\s*(\d+(?:\.\d+)?)', query)
    if match:
        return float(match.group(1))
    
    return None
