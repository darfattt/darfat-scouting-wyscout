"""
Manage chat message history (last 5 messages)
"""
from typing import List, Dict


class ChatMemory:
    """
    Manage chat history for context maintenance
    
    Stores last 5 user/assistant messages
    System prompt is handled separately (not counted in limit)
    """
    
    def __init__(self, max_messages: int = 5):
        """
        Initialize chat memory
        
        Args:
            max_messages: Maximum number of user/assistant messages to keep
        """
        self.max_messages = max_messages
        self.history: List[Dict[str, str]] = []
    
    def add_message(self, role: str, content: str):
        """
        Add message to history
        
        Args:
            role: Either 'user' or 'assistant'
            content: Message content
        """
        self.history.append({'role': role, 'content': content})
        
        if len(self.history) > self.max_messages:
            self.history = self.history[-self.max_messages:]
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get full history (user + assistant messages only)
        
        Returns:
            List of message dicts
        """
        return self.history
    
    def get_last_n(self, n: int) -> List[Dict[str, str]]:
        """
        Get last n messages
        
        Args:
            n: Number of messages to retrieve
        
        Returns:
            List of last n messages
        """
        return self.history[-n:] if len(self.history) >= n else self.history
    
    def clear(self):
        """Clear all history"""
        self.history = []
    
    def get_context_entities(self) -> Dict[str, List[str]]:
        """
        Extract entities mentioned in conversation history
        
        Returns:
            Dict with 'players', 'roles', 'positions' lists
        """
        entities = {'players': [], 'roles': [], 'positions': []}
        
        common_words = {'Find', 'Show', 'Compare', 'Who', 'What', 'How', 'The', 'A', 'An'}
        
        for msg in self.history:
            words = msg['content'].split()
            for i, word in enumerate(words):
                if word[0].isupper() and word not in common_words:
                    if word not in entities['players']:
                        entities['players'].append(word)
        
        return entities
    
    def get_formatted_history(self) -> str:
        """
        Get formatted history string for prompt
        
        Returns:
            Formatted conversation history string
        """
        if not self.history:
            return ""
        
        formatted = "## Conversation History\n"
        for msg in self.history:
            formatted += f"{msg['role']}: {msg['content']}\n"
        
        return formatted
