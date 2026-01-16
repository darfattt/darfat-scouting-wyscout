"""
Parse user queries and extract intent/entities
"""
from typing import Dict, Optional, Tuple
from chatbot.ollama_client.my_ollama_client import MyOllamaClient
from chatbot.utils.parsers import (
    parse_position,
    parse_age_range,
    parse_composite_attribute,
    parse_threshold
)


class QueryProcessor:
    """
    Process user queries and extract intent and entities
    
    Supports:
    - Intent classification (player_lookup, player_finder, comparison, role_analysis, explanation)
    - Entity extraction (players, positions, ages, metrics, thresholds)
    """
    
    def __init__(self, my_ollama_client: MyOllamaClient):
        """
        Initialize query processor
        
        Args:
            my_ollama_client: MyOllamaClient instance for intent classification
        """
        self.client = my_ollama_client
        self.query_types = [
            'player_lookup',
            'player_finder',
            'comparison',
            'role_analysis',
            'explanation',
            'general'
        ]
    
    def process_query(self, query: str) -> Dict:
        """
        Main query processing function
        
        Args:
            query: User query string
        
        Returns:
            {
                'query_type': str,
                'entities': dict,
                'original_query': str
            }
        """
        query_type = self._classify_intent(query)
        entities = self._extract_entities(query, query_type)
        
        return {
            'query_type': query_type,
            'entities': entities,
            'original_query': query
        }
    
    def _classify_intent(self, query: str) -> str:
        """
        Classify intent of query using keyword patterns
        
        Args:
            query: User query string
        
        Returns:
            Intent type string
        """
        query_lower = query.lower()
        
        # Check for player lookup (single player mentioned)
        if any(word in query_lower for word in ['stats', 'show me', 'who is', 'tell me about', 'information']):
            if len(self._extract_potential_players(query)) == 1:
                return 'player_lookup'
        
        # Check for comparison
        if any(word in query_lower for word in ['compare', 'versus', 'vs', 'versus']):
            return 'comparison'
        
        # Check for player finder
        if any(word in query_lower for word in ['find', 'show me', 'list', 'who are', 'search for']):
            return 'player_finder'
        
        # Check for role analysis
        if any(word in query_lower for word in ['role', 'fit', 'profile', 'style', 'best fits']):
            return 'role_analysis'
        
        # Check for explanation
        if any(word in query_lower for word in ['explain', 'what is', 'why', 'how', 'mean']):
            return 'explanation'
        
        return 'general'
    
    def _extract_potential_players(self, query: str) -> list:
        """
        Extract potential player names from query (simple heuristic)
        
        Args:
            query: User query string
        
        Returns:
            List of potential player names
        """
        words = query.split()
        common_words = {
            'find', 'show', 'compare', 'who', 'what', 'how', 'why',
            'is', 'a', 'the', 'for', 'in', 'with', 'about',
            'stats', 'top', 'best', 'list', 'players', 'from'
        }
        
        potential_players = []
        for word in words:
            if (word[0].isupper() and 
                len(word) > 1 and 
                word not in common_words):
                potential_players.append(word)
        
        return potential_players
    
    def _extract_entities(self, query: str, query_type: str) -> Dict:
        """
        Extract entities based on query type
        
        Args:
            query: User query string
            query_type: Classified intent type
        
        Returns:
            Dictionary of extracted entities
        """
        entities = {
            'players': [],
            'players_fuzzy': [],
            'position': None,
            'min_age': None,
            'max_age': None,
            'composite_attr': None,
            'metrics': [],
            'threshold': None
        }
        
        query_lower = query.lower()
        
        # Extract players
        if query_type in ['player_lookup', 'comparison']:
            entities['players'] = self._extract_potential_players(query)
        
        # Extract position
        entities['position'] = parse_position(query)
        
        # Extract age range
        age_range = parse_age_range(query)
        if age_range:
            entities['min_age'], entities['max_age'] = age_range
        
        # Extract composite attribute
        entities['composite_attr'] = parse_composite_attribute(query)
        
        # Extract threshold
        entities['threshold'] = parse_threshold(query)
        
        return entities
