"""
Build retrieval context for LLM
"""
from typing import Dict, List
from chatbot.vector_store.chroma_wrapper import ChromaWrapper
from chatbot.utils.data_formatter import (
    format_player_context,
    format_knowledge_context
)
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class ContextBuilder:
    """
    Assemble retrieval context for LLM from search results
    
    Combines:
    - Player data from vector search
    - Knowledge definitions
    - Role preset information
    """
    
    def __init__(self, chroma_wrapper: ChromaWrapper):
        """
        Initialize context builder
        
        Args:
            chroma_wrapper: ChromaWrapper instance for search
        """
        self.chroma = chroma_wrapper
    
    def build_context(self, query_result: Dict) -> Dict:
        """
        Build complete context for LLM from query results
        
        Args:
            query_result: Dict from QueryProcessor with:
                - query_type
                - entities
                - original_query
        
        Returns:
            {
                'players': List[dict],
                'knowledge': List[dict],
                'roles': List[dict],
                'query_type': str
            }
        """
        query_type = query_result['query_type']
        entities = query_result['entities']
        
        context = {
            'players': [],
            'knowledge': [],
            'roles': [],
            'query_type': query_type
        }
        
        if query_type == 'player_lookup':
            context['players'] = self._get_player_context(entities)
        
        elif query_type == 'player_finder':
            context['players'] = self._search_players(entities)
        
        elif query_type == 'comparison':
            context['players'] = self._search_players(entities)
        
        elif query_type == 'role_analysis':
            context['players'] = self._search_players(entities)
            context['roles'] = self._get_role_context(entities)
        
        elif query_type == 'explanation':
            context['knowledge'] = self._search_knowledge(query_result['original_query'])
        
        return context
    
    def _get_player_context(self, entities: Dict) -> List[Dict]:
        """
        Get context for specific player lookup
        
        Args:
            entities: Extracted entities including player names
        
        Returns:
            List of player contexts
        """
        if not entities['players']:
            return []
        
        players = []
        
        for player_name in entities['players']:
            results = self.chroma.search(
                query=f"Player: {player_name}",
                collection_name="players",
                filters={'player_name': player_name},
                top_k=1
            )
            
            if results['documents']:
                player_context = {
                    'name': player_name,
                    'team': results['metadatas'][0].get('team', 'Unknown'),
                    'position': results['metadatas'][0].get('position', 'Unknown'),
                    'age': results['metadatas'][0].get('age', 0),
                    'league': results['metadatas'][0].get('league', 'Unknown'),
                    'stats': {},
                    'composite_attrs': {}
                }
                players.append(player_context)
        
        return players
    
    def _search_players(self, entities: Dict) -> List[Dict]:
        """
        Search for players matching criteria
        
        Args:
            entities: Extracted entities with filters
        
        Returns:
            List of player contexts
        """
        filters = {}
        
        if entities['position']:
            filters['position'] = entities['position']
        
        if entities['min_age']:
            filters['min_age'] = entities['min_age']
        
        if entities['max_age']:
            filters['max_age'] = entities['max_age']
        
        query = f"Find players"
        
        if entities['composite_attr']:
            query += f" with {entities['composite_attr']} > 80"
            filters['composite_attr'] = entities['composite_attr']
        elif entities['threshold']:
            query += f" with score > {entities['threshold']}"
        
        results = self.chroma.search(
            query=query,
            collection_name="players",
            filters=filters,
            top_k=10
        )
        
        players = []
        
        for doc, meta in zip(results['documents'], results['metadatas']):
            player_context = {
                'name': meta.get('player_name', 'Unknown'),
                'team': meta.get('team', 'Unknown'),
                'position': meta.get('position', 'Unknown'),
                'age': meta.get('age', 0),
                'league': meta.get('league', 'Unknown'),
                'stats': {},
                'composite_attrs': {}
            }
            players.append(player_context)
        
        return players
    
    def _get_role_context(self, entities: Dict) -> List[Dict]:
        """
        Get context for role/preset information
        
        Args:
            entities: Extracted entities
        
        Returns:
            List of role definitions
        """
        if not entities['composite_attr']:
            return []
        
        results = self.chroma.search(
            query=f"Role definition {entities['composite_attr']}",
            collection_name="knowledge",
            filters={'type': 'composite_attribute', 'name': entities['composite_attr']},
            top_k=1
        )
        
        roles = []
        
        if results['documents']:
            roles.append({
                'name': entities['composite_attr'],
                'description': results['documents'][0] if results['documents'] else '',
                'type': 'composite_attribute'
            })
        
        return roles
    
    def _search_knowledge(self, query: str) -> List[Dict]:
        """
        Search knowledge base for explanations
        
        Args:
            query: User query string
        
        Returns:
            List of knowledge items
        """
        results = self.chroma.search(
            query=query,
            collection_name="knowledge",
            top_k=5
        )
        
        knowledge = []
        
        for doc, meta in zip(results['documents'], results['metadatas']):
            knowledge.append({
                'type': meta.get('type', 'unknown'),
                'name': meta.get('name', 'unknown'),
                'display_name': meta.get('display_name', ''),
                'description': meta.get('description', ''),
                'content': doc if doc else ''
            })
        
        return knowledge
