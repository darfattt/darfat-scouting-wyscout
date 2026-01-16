"""
ChromaDB wrapper for vector storage and retrieval
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Any
import pandas as pd
import os
from chatbot.vector_store.embeddings import EmbeddingGenerator


class ChromaWrapper:
    """
    Wrapper for ChromaDB operations
    
    Manages:
    - Player data storage and retrieval
    - Knowledge base storage
    - Role preset storage
    - Semantic search with metadata filters
    """
    
    def __init__(self, persist_directory: str = "chatbot/vector_db"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        self.my_ollama_client = None
        self.embedding_generator = None
    
    def set_ollama_client(self, client):
        """
        Set Ollama client for embedding generation
        
        Args:
            client: MyOllamaClient instance
        """
        self.my_ollama_client = client
        self.embedding_generator = EmbeddingGenerator(client)
    
    def get_or_create_collection(self, name: str):
        """
        Get or create a ChromaDB collection
        
        Args:
            name: Collection name
        
        Returns:
            ChromaDB collection object
        """
        return self.client.get_or_create_collection(name=name)
    
    def index_players(self, df_players: pd.DataFrame, 
                    composite_attrs_df: pd.DataFrame,
                    test_csvs: Optional[List[str]] = None) -> int:
        """
        Index player data from dataframe
        
        Args:
            df_players: DataFrame with all player data
            composite_attrs_df: DataFrame with composite attribute columns
            test_csvs: If provided, only index players from these CSVs
        
        Returns:
            Number of players indexed
        """
        if self.embedding_generator is None:
            raise RuntimeError("Ollama client not set. Call set_ollama_client() first.")
        
        collection = self.get_or_create_collection("players")
        
        documents = []
        metadatas = []
        ids = []
        
        df_merged = df_players.merge(composite_attrs_df, on='Player', how='left', suffixes=('', '_comp'))
        
        for idx, row in df_merged.iterrows():
            doc = self.embedding_generator.generate_player_document(row, {})
            
            documents.append(doc)
            metadatas.append({
                'player_name': row.get('Player', 'Unknown'),
                'team': row.get('Team', 'Unknown'),
                'league': row.get('League', 'Unknown'),
                'position': row.get('Position', 'Unknown'),
                'age': int(row.get('Age', 0)) if pd.notna(row.get('Age')) else 0,
                'minutes': int(row.get('Minutes played', 0)) if pd.notna(row.get('Minutes played')) else 0
            })
            ids.append(f"player_{idx}")
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        return len(documents)
    
    def index_knowledge(self, composite_attributes: Dict, role_presets: Dict) -> int:
        """
        Index knowledge documents (composite attributes and role presets)
        
        Args:
            composite_attributes: COMPOSITE_ATTRIBUTES dictionary
            role_presets: Dictionary of all role presets
        
        Returns:
            Number of knowledge documents indexed
        """
        if self.embedding_generator is None:
            raise RuntimeError("Ollama client not set. Call set_ollama_client() first.")
        
        collection = self.get_or_create_collection("knowledge")
        
        documents = []
        metadatas = []
        ids = []
        
        doc_count = 0
        
        for attr_name, attr_config in composite_attributes.items():
            doc = f"""Composite Attribute: {attr_config['display_name']}
Description: {attr_config['description']}

Components:
"""
            for component in attr_config.get('components', []):
                stat = component.get('stat', 'unknown')
                weight = component.get('weight', 0)
                doc += f"- {stat}: weight={weight}\n"
            
            documents.append(doc)
            metadatas.append({
                'type': 'composite_attribute',
                'name': attr_name,
                'display_name': attr_config['display_name']
            })
            ids.append(f"composite_{attr_name}")
            doc_count += 1
        
        for preset_name, preset_config in role_presets.items():
            doc = f"""Role Preset: {preset_config['display_name']}
Description: {preset_config['description']}

Components:
"""
            for component in preset_config.get('components', []):
                stat = component.get('stat', 'unknown')
                weight = component.get('weight', 0)
                doc += f"- {stat}: weight={weight}\n"
            
            documents.append(doc)
            metadatas.append({
                'type': 'role_preset',
                'name': preset_name,
                'display_name': preset_config['display_name']
            })
            ids.append(f"role_{preset_name}")
            doc_count += 1
        
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        return doc_count
    
    def search(self, query: str, collection_name: str = "players",
              filters: Optional[Dict] = None, top_k: int = 5) -> Dict[str, Any]:
        """
        Search collection with semantic search and optional metadata filters
        
        Args:
            query: Search query text
            collection_name: Name of collection to search
            filters: Metadata filters (e.g., {'position': 'CB', 'min_age': 20})
            top_k: Number of results to return
        
        Returns:
            Dict with 'documents', 'metadatas', 'distances'
        """
        if self.embedding_generator is None:
            raise RuntimeError("Ollama client not set. Call set_ollama_client() first.")
        
        collection = self.get_or_create_collection(collection_name)
        
        query_embedding = self.embedding_generator.generate_document_embedding(query)
        
        where = None
        if filters:
            conditions = []
            
            for key, value in filters.items():
                if value is not None:
                    if key == 'min_age':
                        conditions.append({'age': {'$gte': value}})
                    elif key == 'max_age':
                        conditions.append({'age': {'$lte': value}})
                    elif key == 'min_minutes':
                        conditions.append({'minutes': {'$gte': value}})
                    elif key == 'position':
                        conditions.append({'position': {'$contains': value}})
                    elif key == 'league':
                        conditions.append({'league': value})
            
            if len(conditions) > 1:
                where = {'$and': conditions}
            elif len(conditions) == 1:
                where = conditions[0]
        print(f" query_embedding {query_embedding}")
        print(f"top_k {top_k}")
        print(f"where {where}")
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )
        
        return results
    
    def get_collection_count(self, collection_name: str) -> int:
        """
        Get count of documents in collection
        
        Args:
            collection_name: Name of collection
        
        Returns:
            Number of documents
        """
        collection = self.get_or_create_collection(collection_name)
        return collection.count()
    
    def clear_collection(self, collection_name: str):
        """
        Delete all documents from collection
        
        Args:
            collection_name: Name of collection to clear
        """
        try:
            self.client.delete_collection(name=collection_name)
            self.get_or_create_collection(collection_name)
        except Exception as e:
            pass
