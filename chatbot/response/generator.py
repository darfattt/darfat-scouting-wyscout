"""
Generate responses and select visualizations
"""
from typing import List, Dict
from chatbot.ollama_client.my_ollama_client import MyOllamaClient
from chatbot.response.prompt_builder import build_prompt
from chatbot.utils.viz_utils import (
    create_radar_chart,
    create_comparison_bar,
    create_scatter_plot
)


class ResponseGenerator:
    """
    Generate responses and select appropriate visualizations
    
    Handles:
    - LLM response generation
    - Visualization type selection
    - Chart generation
    """
    
    def __init__(self, my_ollama_client: MyOllamaClient):
        """
        Initialize response generator
        
        Args:
            my_ollama_client: MyOllamaClient instance
        """
        self.client = my_ollama_client
    
    def generate_response(self, query: str, context: Dict, 
                      history: List[Dict[str, str]]) -> Dict:
        """
        Generate complete response with LLM and visualizations
        
        Args:
            query: User's current query
            context: Retrieval context
            history: Chat history (last 5 messages)
        
        Returns:
            {
                'text': str,
                'visualizations': List[plotly.Figure],
                'players_mentioned': List[str]
            }
        """
        prompt = build_prompt(query, context, history)
        
        messages = [
            {'role': 'system', 'content': prompt}
        ]
        
        if history:
            for msg in history:
                messages.append(msg)
        
        messages.append({'role': 'user', 'content': query})
        
        response_text = self.client.generate_chat(messages)
        
        viz_types = self._determine_visualizations(query, context)
        
        visualizations = []
        
        for viz_type in viz_types:
            chart = self._generate_chart(viz_type, context)
            if chart:
                visualizations.append(chart)
        
        players_mentioned = self._extract_players_from_response(response_text)
        
        return {
            'text': response_text,
            'visualizations': visualizations,
            'players_mentioned': players_mentioned
        }
    
    def _determine_visualizations(self, query: str, context: Dict) -> List[str]:
        """
        Determine which visualizations to show based on query
        
        Args:
            query: User query string
            context: Retrieval context with player data
        
        Returns:
            List of visualization types
        """
        viz_types = []
        query_lower = query.lower()
        query_type = context['query_type']
        
        # Auto: player lookup → radar chart
        if query_type == 'player_lookup' and len(context['players']) == 1:
            viz_types.append('radar_profile')
        
        # Keyword: "compare" → comparison bar
        if 'compare' in query_lower and len(context['players']) > 1:
            viz_types.append('comparison_bar')
        
        # Keyword: "similar" → scatter plot
        if 'similar' in query_lower:
            viz_types.append('scatter_similarity')
        
        # Auto: role analysis → role fit chart
        if query_type == 'role_analysis':
            viz_types.append('role_fit')
        
        # Keyword: "show", "display", "chart" → radar for single player
        if any(word in query_lower for word in ['show', 'display', 'chart', 'graph']):
            if len(context['players']) == 1:
                viz_types.append('radar_profile')
        
        return viz_types
    
    def _generate_chart(self, viz_type: str, context: Dict):
        """
        Generate specific chart based on type
        
        Args:
            viz_type: Type of visualization
            context: Retrieval context with player data
        
        Returns:
            Plotly Figure object or None
        """
        if viz_type == 'radar_profile' and len(context['players']) == 1:
            return create_radar_chart(context['players'])
        
        elif viz_type == 'comparison_bar':
            return create_comparison_bar(context['players'])
        
        elif viz_type == 'scatter_similarity':
            if context['players']:
                return create_scatter_plot(context['players'], 'Security', 'ProgPass')
        
        elif viz_type == 'role_fit':
            return create_comparison_bar(context['players'])
        
        return None
    
    def _extract_players_from_response(self, response: str) -> List[str]:
        """
        Extract player names from LLM response
        
        Args:
            response: LLM response text
        
        Returns:
            List of player names mentioned
        """
        words = response.split()
        common_words = {
            'the', 'a', 'an', 'is', 'player', 'players',
            'for', 'with', 'and', 'who', 'what', 'show',
            'find', 'best', 'top', 'list', 'stats', 'data'
        }
        
        players = []
        for word in words:
            if (word[0].isupper() and 
                len(word) > 1 and 
                word not in common_words):
                players.append(word)
        
        return players
