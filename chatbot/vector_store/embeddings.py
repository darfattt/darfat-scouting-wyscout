"""
Generate embeddings using Ollama nomic-embed-text
"""
from typing import List
import pandas as pd
from chatbot.ollama_client.my_ollama_client import MyOllamaClient


class EmbeddingGenerator:
    """
    Generate embeddings for documents using Ollama nomic-embed-text
    """
    
    def __init__(self, my_ollama_client: MyOllamaClient):
        self.client = my_ollama_client
    
    def generate_document_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a document
        
        Args:
            text: Document text to embed
        
        Returns:
            List of floats (embedding vector)
        """
        return self.client.generate_embedding(text)
    
    def generate_batch_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of document texts
        
        Returns:
            List of embedding vectors
        """
        embeddings = []
        for text in texts:
            embedding = self.generate_document_embedding(text)
            embeddings.append(embedding)
        return embeddings
    
    def generate_player_document(self, player_row: pd.Series, composite_attrs: dict) -> str:
        """
        Format player data as searchable document
        
        Args:
            player_row: Pandas Series with player data
            composite_attrs: Dictionary of composite attribute scores
        
        Returns:
            Formatted document string
        """
        doc = f"""Player: {player_row.get('Player', 'Unknown')}
Team: {player_row.get('Team', 'Unknown')}
League: {player_row.get('League', 'Unknown')}
Position: {player_row.get('Position', 'Unknown')}
Age: {player_row.get('Age', 0)}

Key Statistics:
"""
        
        top_stats = [
            'xG per 90', 'Goals per 90', 'Assists per 90',
            'Passes per 90', 'Duels won, %', 'Progressive passes per 90',
            'xA per 90', 'Successful dribbles, %', 'Touches in box per 90'
        ]
        
        for stat in top_stats:
            if stat in player_row:
                value = player_row[stat]
                percentile_col = f"{stat}_percentile"
                percentile = player_row.get(percentile_col, 50) if pd.notna(player_row.get(percentile_col)) else 50
                doc += f"- {stat}: {value:.2f} (percentile: {percentile:.1f})\n"
        
        if composite_attrs:
            doc += "\nComposite Attributes:\n"
            for attr_name, attr_data in composite_attrs.items():
                if isinstance(attr_data, dict) and 'score' in attr_data:
                    doc += f"- {attr_data.get('display_name', attr_name)}: {attr_data['score']:.1f}\n"
        
        return doc
    
    def generate_knowledge_document(self, item: dict) -> str:
        """
        Format knowledge item as searchable document
        
        Args:
            item: Dictionary with type, name, and content
        
        Returns:
            Formatted document string
        """
        item_type = item.get('type', 'unknown')
        name = item.get('name', 'unknown')
        description = item.get('description', '')
        content = item.get('content', '')
        
        doc = f"""Type: {item_type}
Name: {name}

{description}

{content}
"""
        return doc
