"""
Fuzzy matching for player names
"""
from fuzzywuzzy import fuzz, process
from typing import List, Tuple


class FuzzyMatcher:
    """
    Fuzzy match player names using Levenshtein distance
    """
    
    def __init__(self, available_names: List[str]):
        """
        Initialize fuzzy matcher with available player names
        
        Args:
            available_names: List of all player names in database
        """
        self.available_names = available_names
    
    def match(self, query: str, threshold: float = 0.6) -> List[Tuple[str, float]]:
        """
        Find fuzzy matches for player name
        
        Args:
            query: Query string (may contain typos)
            threshold: Minimum similarity score (0-1)
        
        Returns:
            List of (matched_name, score) tuples
        """
        matches = process.extract(
            query,
            self.available_names,
            scorer=fuzz.token_set_ratio,
            limit=5
        )
        
        filtered_matches = [
            (match[0], match[1]/100.0)
            for match in matches
            if match[1]/100.0 >= threshold
        ]
        
        return filtered_matches
    
    def extract_names_from_query(self, query: str) -> List[str]:
        """
        Extract potential player names from query
        
        Args:
            query: User query string
        
        Returns:
            List of potential player names
        """
        common_words = {
            'find', 'show', 'compare', 'who', 'what', 'how', 'the',
            'is', 'a', 'an', 'for', 'in', 'with', 'stats', 'about',
            'top', 'best', 'list', 'players', 'matching', 'fit'
        }
        
        words = []
        current_word = []
        
        for char in query:
            if char.isupper():
                current_word.append(char)
            elif current_word:
                word = ''.join(current_word)
                if word.lower() not in common_words and len(word) > 1:
                    words.append(word)
                current_word = []
        
        if current_word:
            word = ''.join(current_word)
            if word.lower() not in common_words and len(word) > 1:
                words.append(word)
        
        return words
    
    def find_best_match(self, query: str, threshold: float = 0.6) -> Optional[str]:
        """
        Find single best matching player name
        
        Args:
            query: Query string
            threshold: Minimum similarity score
        
        Returns:
            Best matching name or None
        """
        matches = self.match(query, threshold)
        
        if matches:
            return matches[0][0]
        
        return None
