"""
Player similarity calculation using weighted cosine similarity
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from sklearn.metrics.pairwise import cosine_similarity


class SimilarityScorer:
    """
    Calculate player-to-player similarity using weighted metrics
    """

    def __init__(self, df: pd.DataFrame, stat_columns: List[str], composite_columns: List[str] = None):
        """
        Initialize scorer with dataset

        Args:
            df: Player dataframe with all statistics
            stat_columns: List of metric columns to use for similarity
            composite_columns: List of composite attribute columns (e.g., COMP_Security)
        """
        self.df = df.copy()
        self.stat_columns = stat_columns
        self.composite_columns = composite_columns if composite_columns else []
        self.all_selectable_columns = stat_columns + self.composite_columns
        self.negative_metrics = [
            'Fouls per 90',
            'Cards per 90',
            'Conceded goals per 90'
        ]  # Metrics where lower is better

    def calculate_similarity(
        self,
        reference_player_name: str,
        weights: Dict[str, float],
        min_minutes: int = 0,
        age_range: Tuple[int, int] = (15, 40),
        league_weights: Dict[str, float] = None,
        same_position_only: bool = True,
        top_n: int = 30,
        contract_expired: bool = None
    ) -> pd.DataFrame:
        """
        Find most similar players to reference player

        Args:
            reference_player_name: Name of reference player
            weights: Dictionary of {metric: weight} for similarity calculation
            min_minutes: Minimum minutes played filter
            age_range: (min_age, max_age) tuple
            league_weights: Dictionary of {league: multiplier} for weighting leagues
            same_position_only: If True, only compare to players in same position
            top_n: Number of top similar players to return
            contract_expired: Filter by contract expiry (True = expired only, False/None = all players)

        Returns:
            DataFrame with top N similar players and similarity scores
        """
        # STEP 1: Get reference player
        ref_player = self.df[self.df['Player'] == reference_player_name]
        if len(ref_player) == 0:
            raise ValueError(f"Player '{reference_player_name}' not found")
        ref_player = ref_player.iloc[0]

        # STEP 2: Apply filters to candidate pool
        candidates = self.df.copy()

        # Exclude reference player from candidates
        candidates = candidates[candidates['Player'] != reference_player_name]

        # Minutes filter (if Minutes column exists)
        if 'Minutes' in candidates.columns:
            candidates = candidates[candidates['Minutes'] >= min_minutes]

        # Age filter
        if 'Age' in candidates.columns:
            min_age, max_age = age_range
            candidates = candidates[(candidates['Age'] >= min_age) &
                                  (candidates['Age'] <= max_age)]

        # Same position filter
        if same_position_only and 'Position' in candidates.columns:
            ref_position = ref_player['Position']
            candidates = candidates[candidates['Position'] == ref_position]

        # Contract expiry filter
        if contract_expired is True and 'contract_expiry' in candidates.columns:
            candidates = candidates[candidates['contract_expiry'] == True]

        if len(candidates) == 0:
            # Return empty dataframe with expected columns
            return pd.DataFrame(columns=[
                'Rank', 'Player', 'Team', 'Position', 'Age',
                'Similarity_Score', 'Similarity_Percentile'
            ])

        # STEP 3: Filter weights to only valid metrics
        valid_weights = {k: v for k, v in weights.items()
                        if k in self.all_selectable_columns and k in candidates.columns}

        if not valid_weights:
            raise ValueError("No valid metrics found for similarity calculation")

        # Normalize weights to sum to 1.0
        total_weight = sum(abs(w) for w in valid_weights.values())
        normalized_weights = {k: v/total_weight for k, v in valid_weights.items()}

        # STEP 4: Calculate weighted similarity
        metric_names = list(normalized_weights.keys())

        # Extract and normalize metric values
        ref_vector = []
        candidate_vectors = []

        for metric in metric_names:
            # Get values
            ref_val = ref_player[metric]
            cand_vals = candidates[metric].values

            # Handle NaN
            if pd.isna(ref_val):
                ref_val = 0
            cand_vals = np.nan_to_num(cand_vals, 0)

            # Normalize to 0-100 scale for consistency
            all_vals = np.append(cand_vals, ref_val)
            val_min = all_vals.min()
            val_max = all_vals.max()

            if val_max == val_min:
                ref_normalized = 50.0
                cand_normalized = np.full(len(cand_vals), 50.0)
            else:
                # Invert for negative metrics
                if metric in self.negative_metrics:
                    ref_normalized = 100 - ((ref_val - val_min) / (val_max - val_min) * 100)
                    cand_normalized = 100 - ((cand_vals - val_min) / (val_max - val_min) * 100)
                else:
                    ref_normalized = (ref_val - val_min) / (val_max - val_min) * 100
                    cand_normalized = (cand_vals - val_min) / (val_max - val_min) * 100

            # Apply weight
            weight = normalized_weights[metric]
            ref_vector.append(ref_normalized * weight)
            candidate_vectors.append(cand_normalized * weight)

        # Convert to numpy arrays
        ref_vector = np.array(ref_vector).reshape(1, -1)
        candidate_matrix = np.array(candidate_vectors).T

        # Calculate cosine similarity
        similarities = cosine_similarity(ref_vector, candidate_matrix)[0]

        # STEP 5: Apply league weights if provided
        if league_weights and 'League' in candidates.columns:
            league_multipliers = candidates['League'].map(league_weights).fillna(1.0).values
            similarities = similarities * league_multipliers

        # STEP 6: Add similarity scores to candidates
        candidates = candidates.copy()
        candidates['Similarity_Score'] = similarities

        # Calculate percentile (avoid division by zero)
        max_sim = similarities.max()
        if max_sim > 0:
            candidates['Similarity_Percentile'] = similarities / max_sim * 100
        else:
            candidates['Similarity_Percentile'] = 50.0

        # STEP 7: Sort and return top N
        result = candidates.sort_values('Similarity_Score', ascending=False).head(top_n)
        result['Rank'] = range(1, len(result) + 1)

        # Select relevant columns
        display_cols = ['Rank', 'Player', 'Team', 'Position', 'Age', 'contract_expiry',
                       'Similarity_Score', 'Similarity_Percentile'] + metric_names

        # Filter to only existing columns
        display_cols = [col for col in display_cols if col in result.columns]

        return result[display_cols].reset_index(drop=True)

    def get_metric_contributions(
        self,
        reference_player_name: str,
        similar_player_name: str,
        weights: Dict[str, float]
    ) -> Dict[str, Dict]:
        """
        Get detailed metric breakdown for why two players are similar

        Args:
            reference_player_name: Reference player
            similar_player_name: Player to compare to
            weights: Metric weights used

        Returns:
            Dictionary with metric-by-metric comparison
        """
        ref_player = self.df[self.df['Player'] == reference_player_name].iloc[0]
        sim_player = self.df[self.df['Player'] == similar_player_name].iloc[0]

        contributions = {}

        for metric, weight in weights.items():
            if metric not in self.stat_columns or metric not in self.df.columns:
                continue

            ref_val = ref_player[metric]
            sim_val = sim_player[metric]

            # Handle NaN values
            if pd.isna(ref_val):
                ref_val = 0
            if pd.isna(sim_val):
                sim_val = 0

            # Calculate difference
            diff = abs(ref_val - sim_val)

            # Calculate similarity for this metric (1 - normalized difference)
            max_diff = self.df[metric].max() - self.df[metric].min()
            if max_diff > 0:
                metric_similarity = 1 - (diff / max_diff)
            else:
                metric_similarity = 1.0

            # Ensure similarity is in valid range
            metric_similarity = max(0, min(1, metric_similarity))

            contributions[metric] = {
                'reference_value': ref_val,
                'similar_value': sim_val,
                'difference': diff,
                'metric_similarity': metric_similarity * 100,  # 0-100 scale
                'weight': weight,
                'weighted_contribution': metric_similarity * abs(weight) * 100
            }

        return contributions

    def get_composite_contributions(
        self,
        reference_player_name: str,
        similar_player_name: str,
        weights: Dict[str, float],
        composite_attributes: Dict
    ) -> Dict[str, Dict]:
        """
        Get detailed composite attribute breakdown for similarity comparison

        Similar to get_metric_contributions() but for composite attributes (COMP_* columns)

        Args:
            reference_player_name: Reference player name
            similar_player_name: Player to compare against
            weights: Metric weights dict (should include COMP_* keys)
            composite_attributes: COMPOSITE_ATTRIBUTES config from config/composite_attributes.py

        Returns:
            Dictionary with composite-by-composite comparison:
            {
                'COMP_Tackling': {
                    'display_name': '🛡️ Tackling',
                    'reference_value': 85.2,
                    'similar_value': 82.7,
                    'difference': 2.5,
                    'metric_similarity': 92.3,  # 0-100 scale
                    'weight': 0.25,
                    'weighted_contribution': 23.075
                },
                ...
            }
        """
        # STEP 1: Get both players from DataFrame
        ref_player = self.df[self.df['Player'] == reference_player_name]
        sim_player = self.df[self.df['Player'] == similar_player_name]

        if len(ref_player) == 0:
            raise ValueError(f"Reference player '{reference_player_name}' not found")
        if len(sim_player) == 0:
            raise ValueError(f"Similar player '{similar_player_name}' not found")

        ref_player = ref_player.iloc[0]
        sim_player = sim_player.iloc[0]

        contributions = {}

        # STEP 2: Filter weights to only composite attributes
        composite_weights = {k: v for k, v in weights.items() if k.startswith('COMP_')}

        if not composite_weights:
            return {}  # No composite attributes selected

        # STEP 3: Calculate contribution for each composite attribute
        for comp_col, weight in composite_weights.items():
            # Extract attribute key: COMP_Tackling → Tackling
            attr_key = comp_col.replace('COMP_', '')

            # Verify column exists in DataFrame
            if comp_col not in self.df.columns:
                continue

            # Get values for both players
            ref_val = ref_player[comp_col]
            sim_val = sim_player[comp_col]

            # Handle NaN (use percentile=50 as default)
            if pd.isna(ref_val):
                ref_val = 50.0
            if pd.isna(sim_val):
                sim_val = 50.0

            # Calculate absolute difference
            diff = abs(ref_val - sim_val)

            # Calculate metric similarity (1 - normalized difference)
            # PATTERN: Same as get_metric_contributions() lines 218-222
            max_diff = self.df[comp_col].max() - self.df[comp_col].min()
            if max_diff > 0:
                metric_similarity = 1 - (diff / max_diff)
            else:
                metric_similarity = 1.0  # No variance in dataset

            # Clamp to [0, 1] range
            metric_similarity = max(0, min(1, metric_similarity))

            # Get display metadata from composite_attributes config
            attr_config = composite_attributes.get(attr_key, {})
            display_name = attr_config.get('display_name', attr_key)
            icon = attr_config.get('icon', '')

            # Store contribution data
            contributions[comp_col] = {
                'display_name': f"{icon} {display_name}".strip(),
                'reference_value': float(ref_val),
                'similar_value': float(sim_val),
                'difference': float(diff),
                'metric_similarity': float(metric_similarity * 100),  # Convert to percentage
                'weight': float(weight),
                'weighted_contribution': float(metric_similarity * abs(weight) * 100)
            }

        return contributions

    def get_all_composite_contributions(
        self,
        reference_player_name: str,
        similar_player_name: str,
        composite_attributes: Dict
    ) -> Dict[str, Dict]:
        """
        Get ALL composite attribute contributions (not filtered by weights)

        Args:
            reference_player_name: Reference player name
            similar_player_name: Player to compare against
            composite_attributes: COMPOSITE_ATTRIBUTES config from config/composite_attributes.py

        Returns:
            Dictionary with ALL composite-by-composite comparison
        """
        ref_player = self.df[self.df['Player'] == reference_player_name]
        sim_player = self.df[self.df['Player'] == similar_player_name]

        if len(ref_player) == 0:
            raise ValueError(f"Reference player '{reference_player_name}' not found")
        if len(sim_player) == 0:
            raise ValueError(f"Similar player '{similar_player_name}' not found")

        ref_player = ref_player.iloc[0]
        sim_player = sim_player.iloc[0]

        contributions = {}

        for attr_key, attr_config in composite_attributes.items():
            comp_col = f"COMP_{attr_key}"

            if comp_col not in self.df.columns:
                continue

            ref_val = ref_player[comp_col]
            sim_val = sim_player[comp_col]

            ref_val = 50.0 if pd.isna(ref_val) else float(ref_val)
            sim_val = 50.0 if pd.isna(sim_val) else float(sim_val)

            diff = abs(ref_val - sim_val)
            max_diff = self.df[comp_col].max() - self.df[comp_col].min()

            if max_diff > 0:
                metric_similarity = 1 - (diff / max_diff)
            else:
                metric_similarity = 1.0

            metric_similarity = max(0, min(1, metric_similarity))

            display_name = attr_config.get('display_name', attr_key)
            icon = attr_config.get('icon', '')

            contributions[comp_col] = {
                'display_name': f"{icon} {display_name}".strip(),
                'reference_value': ref_val,
                'similar_value': sim_val,
                'difference': diff,
                'metric_similarity': float(metric_similarity * 100)
            }

        return contributions
