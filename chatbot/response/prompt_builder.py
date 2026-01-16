"""
Construct LLM prompts
"""
from typing import List, Dict
from chatbot.knowledge.system_prompts import (
    SYSTEM_PROMPT,
    PLAYER_LOOKUP_PROMPT,
    PLAYER_FINDER_PROMPT,
    COMPARISON_PROMPT,
    ROLE_ANALYSIS_PROMPT,
    EXPLANATION_PROMPT
)
from chatbot.utils.data_formatter import (
    format_player_context,
    format_knowledge_context
)


def build_prompt(query: str, context: Dict, history: List[Dict[str, str]]) -> str:
    """
    Construct full prompt for LLM
    
    Args:
        query: User's current query
        context: Retrieval context with players, knowledge, roles
        history: List of previous user/assistant messages (max 5)
    
    Returns:
        Complete prompt string for LLM
    """
    prompt = SYSTEM_PROMPT + "\n\n"
    
    if history:
        prompt += history[0].get('formatted', history[0]) + "\n\n"
    
    prompt += "## Retrieved Context\n\n"
    
    if context['players']:
        prompt += "### Available Player Data\n\n"
        for player in context['players']:
            prompt += format_player_context(player) + "\n"
    
    if context['knowledge']:
        prompt += "### Knowledge Base\n\n"
        for item in context['knowledge']:
            prompt += format_knowledge_context(item) + "\n"
    
    if context['roles']:
        prompt += "### Role Definitions\n\n"
        for role in context['roles']:
            prompt += f"**{role['name']}**: {role.get('description', '')}\n"
    
    prompt += f"\n## Current Query\n{query}\n\n"
    prompt += "Provide a comprehensive, scout-style answer based on the data above."
    
    return prompt


def format_history(history: List[Dict[str, str]]) -> str:
    """
    Format chat history for prompt inclusion
    
    Args:
        history: List of message dicts with 'role' and 'content'
    
    Returns:
        Formatted history string
    """
    if not history:
        return ""
    
    formatted = "## Conversation History\n"
    for msg in history:
        formatted += f"{msg['role']}: {msg['content']}\n"
    
    return formatted
