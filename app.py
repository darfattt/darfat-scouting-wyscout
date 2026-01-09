"""
Streamlit app for football player comparison and player finder
Multi-league scouting tool with defender profile analysis
"""
import streamlit as st
import os
from config.stat_categories import STAT_CATEGORIES, PLAYER_INFO_COLUMNS, PLAYER_COLORS
from config.composite_attributes import COMPOSITE_ATTRIBUTES
from config.defender_presets import DEFENDER_PRESETS
from config.forward_presets import FORWARD_PRESETS
from config.position_groups import POSITION_GROUPS, get_position_group_options
from utils.data_loader import prepare_data_global, get_player_info, get_player_stats, get_all_stat_columns, calculate_composite_attributes, get_player_composite_attrs, get_distinct_values, filter_players
from utils.player_comparison import display_player_comparison, create_stats_table, display_composite_attributes, display_position_based_rankings
from utils.player_finder import show_player_finder
from utils.player_similarity import SimilarityScorer
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Player Scouting Hub",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
# st.markdown("""
# <style>
#     .main {
#         background-color: #f5f3e8;
#     }
#     .stSelectbox {
#         background-color: white;
#     }
#     h1 {
#         color: #2c3e50;
#         font-weight: 700;
#     }
#     h2, h3 {
#         color: #34495e;
#     }
# </style>
# """, unsafe_allow_html=True)


@st.cache_data
def load_global_data():
    """
    Load and cache ALL player data from all leagues
    Percentiles calculated globally across all players
    """
    data_folder = os.path.join(os.getcwd(), "data", "2025")

    if not os.path.exists(data_folder):
        st.error(f"Data folder not found: {data_folder}")
        st.stop()

    return prepare_data_global(data_folder, STAT_CATEGORIES)


def build_custom_preset_ui():
    """
    Build custom preset configuration in main content area

    Returns:
        Dictionary matching DEFENDER_PRESETS structure or None if no metrics added
    """
    st.markdown("#### 🛠️ Custom Preset Builder")

    # Initialize session state
    if 'custom_metrics' not in st.session_state:
        st.session_state.custom_metrics = []

    with st.expander("⚙️ Configure Metrics", expanded=True):
        # Preset name and description
        preset_name = st.text_input(
            "Preset Name:",
            value="My Custom Preset",
            key="custom_preset_name"
        )

        preset_description = st.text_area(
            "Description:",
            value="Custom weighted scoring profile",
            height=60,
            key="custom_preset_description"
        )

        st.markdown("---")
        st.markdown("**Add Metrics:**")

        # Get all available stats
        all_stats = get_all_stat_columns(STAT_CATEGORIES)

        # Metric selector
        selected_metric = st.selectbox(
            "Choose a metric:",
            options=[""] + all_stats,
            key="metric_selector"
        )

        col1, col2 = st.columns([3, 1])
        with col1:
            metric_weight = st.number_input(
                "Weight:",
                min_value=-1.0,
                max_value=1.0,
                value=0.25,
                step=0.05,
                help="Negative weights invert metric (lower is better)",
                key="metric_weight_input"
            )

        with col2:
            if st.button("➕ Add", key="add_metric_btn"):
                if selected_metric and selected_metric != "":
                    # Check if metric already added
                    existing_metrics = [m['stat'] for m in st.session_state.custom_metrics]
                    if selected_metric not in existing_metrics:
                        st.session_state.custom_metrics.append({
                            'stat': selected_metric,
                            'weight': metric_weight
                        })
                        st.rerun()
                    else:
                        st.warning(f"'{selected_metric}' already added")

        st.markdown("---")
        st.markdown("**Selected Metrics:**")

        # Display current metrics
        if len(st.session_state.custom_metrics) == 0:
            st.info("No metrics added yet. Add at least 1 metric.")
        else:
            for i, metric_config in enumerate(st.session_state.custom_metrics):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.text(metric_config['stat'][:30])  # Truncate long names
                with col2:
                    st.text(f"Weight: {metric_config['weight']:.2f}")
                with col3:
                    if st.button("🗑️", key=f"remove_metric_{i}"):
                        st.session_state.custom_metrics.pop(i)
                        st.rerun()

        st.markdown("---")

        # Summary
        total_weight = sum(abs(m['weight']) for m in st.session_state.custom_metrics)
        st.metric("Total Metrics", len(st.session_state.custom_metrics))
        st.metric("Total Weight (abs)", f"{total_weight:.2f}")

        # Clear all button
        if st.button("🔄 Clear All Metrics", key="clear_all_metrics"):
            st.session_state.custom_metrics = []
            st.rerun()

    # Return preset configuration
    if len(st.session_state.custom_metrics) == 0:
        return None

    return {
        'display_name': preset_name,
        'description': preset_description,
        'components': st.session_state.custom_metrics,
        'icon': '🎯'  # Default icon for custom presets
    }


def render_player_comparison_page(df_filtered):
    """
    Render Player Comparison page content

    Args:
        df_filtered: Filtered player dataframe
    """
    st.header("⚽ Player Comparison")

    if len(df_filtered) == 0:
        st.warning("⚠️ No players match the selected filters. Adjust global filters in sidebar.")
        return

    # ========== PAGE OPTIONS SECTION ==========
    st.markdown("### ⚙️ Page Options")

    col1, col2 = st.columns([2, 1])
    with col1:
        if len(df_filtered) > 0:
            player_names = sorted(df_filtered['Player'].tolist())
            selected_players = st.multiselect(
                "Choose players (2-3):",
                options=player_names,
                max_selections=3,
                help="Select 2-3 players to compare",
                key="selected_players"
            )
        else:
            selected_players = []
            st.warning("No players available")

    with col2:
        st.info(f"📊 {len(df_filtered)} players available")

    st.markdown("---")

    # Show instructions if no players selected
    if len(selected_players) == 0:
        st.info("☝️ Please select at least 2 players from above to begin comparison.")

        # Show stats about the FILTERED dataset
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filtered Players", len(df_filtered))
        with col2:
            avg_age = df_filtered[PLAYER_INFO_COLUMNS['age']].mean()
            st.metric("Average Age", f"{avg_age:.1f}")
        with col3:
            num_teams = df_filtered[PLAYER_INFO_COLUMNS['team']].nunique()
            st.metric("Teams", num_teams)

        st.markdown("---")
        st.markdown("#### Available Players")
        st.dataframe(
            df_filtered[[
                PLAYER_INFO_COLUMNS['name'],
                PLAYER_INFO_COLUMNS['age'],
                PLAYER_INFO_COLUMNS['team'],
                PLAYER_INFO_COLUMNS['position'],
                PLAYER_INFO_COLUMNS['country']
            ]].sort_values(PLAYER_INFO_COLUMNS['name']),
            use_container_width=True,
            hide_index=True
        )
    elif len(selected_players) < 2:
        st.warning("⚠️ Please select at least 2 players to compare.")
    else:
        # Prepare player data
        players_data = []
        stat_columns = get_all_stat_columns(STAT_CATEGORIES)

        for player_name in selected_players:
            player_info = get_player_info(df_filtered, player_name, PLAYER_INFO_COLUMNS)
            player_stats = get_player_stats(df_filtered, player_name, stat_columns)

            # Calculate composite attributes
            composite_attrs = calculate_composite_attributes(player_stats, COMPOSITE_ATTRIBUTES)

            players_data.append({
                'info': player_info,
                'stats': player_stats,
                'composite_attributes': composite_attrs
            })

        # Display comparison
        display_player_comparison(players_data, STAT_CATEGORIES, PLAYER_COLORS[:len(selected_players)])

        # Display composite attributes
        display_composite_attributes(players_data, PLAYER_COLORS[:len(selected_players)])

        # Infer position type from selected players for position-based rankings
        first_player_position = players_data[0]['info']['position']

        # Simple position mapping
        if 'CB' in first_player_position or 'LCB' in first_player_position or 'RCB' in first_player_position:
            inferred_position_type = 'CB'
        elif 'DMF' in first_player_position or 'CMF' in first_player_position or 'DM' in first_player_position or 'CM' in first_player_position:
            inferred_position_type = 'DM/CM'
        else:
            # Default to DM/CM for other positions
            inferred_position_type = 'DM/CM'

        # Display position-based rankings
        display_position_based_rankings(players_data, inferred_position_type, PLAYER_COLORS[:len(selected_players)])

        # Optional: Show detailed statistics table
        with st.expander("📊 View Detailed Statistics Table"):
            create_stats_table(players_data, STAT_CATEGORIES)


def get_relevant_presets(df_filtered):
    """
    Get relevant presets based on the position groups present in filtered data
    
    Args:
        df_filtered: Filtered player dataframe
    
    Returns:
        Dict of relevant presets
    """
    from config.position_groups import POSITION_GROUPS
    
    # Check what positions are in the filtered data
    positions_in_data = df_filtered['Position'].unique()
    
    # Determine if data contains forward or defender positions
    has_forwards = any(pos in positions_in_data for pos in ['CF', 'CF, AMF', 'CF, LW', 'CF, RW', 'CF, LWF', 'CF, RWF'])
    has_defenders = any(pos in positions_in_data for pos in ['CB', 'LB', 'RB', 'CDM', 'DMF'])
    
    if has_forwards and has_defenders:
        # Mixed data - provide all presets
        all_presets = {}
        all_presets.update(DEFENDER_PRESETS)
        all_presets.update(FORWARD_PRESETS)
        return all_presets
    elif has_forwards:
        # Forward only data
        return FORWARD_PRESETS
    else:
        # Defender only data
        return DEFENDER_PRESETS


def render_player_finder_page(df_filtered):
    """
    Render Player Finder page content with interactive weight adjustment

    Args:
        df_filtered: Filtered player dataframe
    """
    st.header("🎯 Player Finder")

    if len(df_filtered) == 0:
        st.warning("⚠️ No players match the selected filters. Adjust global filters in sidebar.")
        return

    # ========== PAGE OPTIONS SECTION ==========
    st.markdown("### ⚙️ Select Profile")

    col1, col2 = st.columns([3, 1])

    # Get relevant presets based on position data
    relevant_presets = get_relevant_presets(df_filtered)
    
    with col1:
        selected_preset = st.selectbox(
            "Choose a player profile:",
            options=list(relevant_presets.keys()),
            help="Select a preset to start with. You can adjust weights below.",
            key="preset_selection"
        )

    with col2:
        st.info(f"📊 {len(df_filtered)} players available")

    # Show preset info
    preset_info = relevant_presets[selected_preset]
    st.info(f"{preset_info['icon']} **{preset_info['display_name']}** - {preset_info['description']}")

    st.markdown("---")

    # ========== WEIGHT ADJUSTMENT SECTION ==========
    st.markdown("### ⚖️ Adjust Metric Weights")

    # Get preset metrics and all available stats
    preset_metrics = {comp['stat']: comp['weight'] for comp in preset_info['components']}
    all_stats = get_all_stat_columns(STAT_CATEGORIES)

    # Two-column layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("#### Preset Metrics")
        adjusted_weights = {}

        for metric, default_weight in preset_metrics.items():
            if metric in df_filtered.columns:
                adjusted_weights[metric] = st.slider(
                    metric,
                    min_value=-1.0,
                    max_value=1.0,
                    value=default_weight,
                    step=0.05,
                    help=f"Weight for {metric} (default: {default_weight})",
                    key=f"preset_{metric}"
                )
            else:
                st.warning(f"⚠️ {metric} not available in dataset")

    with col2:
        st.markdown("#### ➕ Other Metrics")
        with st.expander("Customize with additional metrics"):
            other_metrics = [m for m in all_stats if m not in preset_metrics.keys() and m in df_filtered.columns]

            if other_metrics:
                additional_weights = {}

                # Group in columns
                metric_cols = st.columns(2)
                for i, metric in enumerate(other_metrics):
                    with metric_cols[i % 2]:
                        include = st.checkbox(metric, key=f"include_{metric}")
                        if include:
                            weight = st.slider(
                                "Weight",
                                min_value=-1.0,
                                max_value=1.0,
                                value=0.1,
                                step=0.05,
                                key=f"weight_{metric}"
                            )
                            additional_weights[metric] = weight
            else:
                st.info("All metrics already included in preset")
                additional_weights = {}

    # Weight summary
    total_weight = sum(abs(w) for w in adjusted_weights.values())
    if additional_weights:
        total_weight += sum(abs(w) for w in additional_weights.values())

    st.info(f"**Total Weight**: {total_weight:.2f} (will be normalized)")

    st.markdown("---")

    # ========== CALCULATE BUTTON ==========
    if st.button("🔄 Calculate Profile Scores", type="primary"):
        if total_weight == 0:
            st.error("❌ Please set at least one metric weight greater than 0")
        else:
            # Combine weights
            all_weights = adjusted_weights.copy()
            if additional_weights:
                all_weights.update(additional_weights)

            # Create temp preset for calculation
            temp_preset_config = {
                'display_name': preset_info['display_name'],
                'description': preset_info['description'],
                'components': [{'stat': k, 'weight': v} for k, v in all_weights.items()],
                'icon': preset_info['icon']
            }

            # Display results
            show_player_finder(df_filtered, {selected_preset: temp_preset_config}, selected_preset)


def get_top_stats_with_weights(df_filtered: pd.DataFrame, selected_player: str, player_position: str, top_n: int = 10) -> dict:
    """
    Get top individual stats for a position with weights based on player's actual stat values

    Args:
        df_filtered: Filtered player dataframe
        selected_player: Name of selected player
        player_position: Player position (e.g., "CB", "AM")
        top_n: Number of top stats to return (default: 10)

    Returns:
        Dict of {stat_name: weight} for top stats
    """
    from config.position_rankings import POSITION_RANKINGS
    from config.position_groups import POSITION_GROUPS
    from utils.data_loader import get_player_stats
    from config.stat_categories import STAT_CATEGORIES
    from config.composite_attributes import COMPOSITE_ATTRIBUTES

    stat_columns = get_all_stat_columns(STAT_CATEGORIES)

    position_group = None
    for pos_group, pos_list in POSITION_GROUPS.items():
        if pos_list and player_position in pos_list:
            for rank_group in POSITION_RANKINGS.keys():
                if rank_group in pos_group or pos_group in rank_group:
                    position_group = rank_group
                    break
        if position_group:
            break

    if not position_group:
        position_group = list(POSITION_RANKINGS.keys())[0]

    key_composites = POSITION_RANKINGS[position_group]["key_attributes"]

    all_candidate_stats = set()
    for comp_attr in key_composites:
        if comp_attr not in COMPOSITE_ATTRIBUTES:
            continue
        components = COMPOSITE_ATTRIBUTES[comp_attr].get("components", [])
        for comp in components:
            stat_name = comp["stat"]
            if stat_name in stat_columns:
                all_candidate_stats.add(stat_name)

    player_stats = get_player_stats(df_filtered, selected_player, list(all_candidate_stats))

    stat_percentiles = {}
    for stat_name in all_candidate_stats:
        if stat_name in player_stats:
            stat_percentiles[stat_name] = player_stats[stat_name].get('percentile', 50.0)
        else:
            stat_percentiles[stat_name] = 50.0

    sorted_stats = sorted(stat_percentiles.items(), key=lambda x: x[1], reverse=True)
    top_stats = sorted_stats[:top_n]

    total_percentile = sum(stat[1] for stat in top_stats)

    if total_percentile > 0:
        weights = {stat[0]: stat[1] / total_percentile for stat in top_stats}
    else:
        weights = {stat[0]: 1.0 / len(top_stats) for stat in top_stats}

    return weights


def render_player_similarity_page(df_filtered):
    """
    Render Player Similarity page content

    Args:
        df_filtered: Filtered player dataframe from global filters
    """
    import plotly.graph_objects as go
    import plotly.express as px

    st.header("🔍 Player Similarity")

    if len(df_filtered) == 0:
        st.warning("⚠️ No players match the selected filters. Adjust global filters in sidebar.")
        return

    # ========== PAGE OPTIONS SECTION ==========

    col1, col2 = st.columns([3, 1])
    

    with col1:
        default_player = 'F. Barba'
        player_names = sorted(df_filtered['Player'].tolist())

        default_index = (
            player_names.index(default_player)
            if default_player in player_names
            else 0
        )
        # Player selection dropdown
        selected_player = st.selectbox(
            "Choose a reference player:",
            options=player_names,
            index=default_index,
            help="Find players similar to this reference player",
            key="similarity_reference_player"
        )

    #with col2:
    
    #st.info(f"📊 {len(df_filtered)} players available")
    if not selected_player:
        st.info("☝️ Please select a reference player to begin similarity analysis.")
        return

    # Show reference player info
    ref_player_info = df_filtered[df_filtered['Player'] == selected_player].iloc[0]
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Player", selected_player)
    with col2:
        st.metric("Team", ref_player_info['Team'])
    with col3:
        st.metric("Position", ref_player_info['Position'])
    with col4:
        st.metric("Age", ref_player_info['Age'])

    st.markdown("---")

    # Display reference player's composite attributes (pre-calculated in dataframe)
    from utils.data_loader import get_player_composite_attrs
    from config.composite_attributes import COMPOSITE_ATTRIBUTES

    # Get stat columns for individual metrics
    stat_columns = get_all_stat_columns(STAT_CATEGORIES)

    with st.expander("⚙️ Reference Player Attributes", expanded=False):
        # Get composite attributes directly from dataframe
        ref_composite_attrs = get_player_composite_attrs(df_filtered, selected_player, COMPOSITE_ATTRIBUTES)

        # Display attributes
        if ref_composite_attrs:
            comp_cols = st.columns(4)
            for idx, (attr_key, attr_data) in enumerate(ref_composite_attrs.items()):
                with comp_cols[idx % 4]:
                    st.metric(
                        label=f"{attr_data['icon']} {attr_data['display_name']}",
                        value=f"{attr_data['score']:.1f}",
                        help=attr_data['description']
                    )

    st.markdown("---")

    # ========== METRIC WEIGHTS SECTION ==========
    st.markdown("### ⚖️ Adjust Metric Weights")

    from config.composite_attributes import COMPOSITE_ATTRIBUTES
    from config.position_rankings import POSITION_RANKINGS

    player_position = ref_player_info['Position']

    position_group = None
    for pos_group, pos_list in POSITION_GROUPS.items():
        if pos_list and player_position in pos_list:
            for rank_group in POSITION_RANKINGS.keys():
                if rank_group in pos_group or pos_group in rank_group:
                    position_group = rank_group
                    break
        if position_group:
            break

    if not position_group:
        position_group = list(POSITION_RANKINGS.keys())[0]

    relevant_composites = POSITION_RANKINGS[position_group]["key_attributes"]
    composite_columns = [f"COMP_{attr}" for attr in COMPOSITE_ATTRIBUTES.keys()]

    composite_display_names = {
        f"COMP_{key}": f"{config.get('icon', '')} {config['display_name']}"
        for key, config in COMPOSITE_ATTRIBUTES.items()
    }

    if 'selected_player' not in st.session_state or st.session_state.selected_player != selected_player:
        top_stats_weights = get_top_stats_with_weights(df_filtered, selected_player, player_position, top_n=10)
        st.session_state.similarity_weights = top_stats_weights
        st.session_state.selected_player = selected_player

    if 'similarity_weights' not in st.session_state:
        st.session_state.similarity_weights = get_top_stats_with_weights(
            df_filtered, selected_player, player_position, top_n=10
        )

    with st.expander("⚙️ Configure Metric Weights", expanded=True):
        adjusted_weights = {}

        metric_tab1, metric_tab2 = st.tabs(["📊 Individual Stats", "🎯 Attributes"])

        with metric_tab1:
            st.markdown("#### Individual Statistics")
            st.caption("Weights based on your selected player's stat percentiles. Higher stats = more influence on similarity.")

            current_individual_weights = {
                k: v for k, v in st.session_state.similarity_weights.items()
                if k in stat_columns
            }

            if current_individual_weights:
                for metric, default_weight in current_individual_weights.items():
                    weight = st.slider(
                        metric,
                        min_value=0.0,
                        max_value=1.0,
                        value=default_weight,
                        step=0.05,
                        key=f"sim_weight_ind_{metric}",
                        help=f"Current weight: {default_weight:.3f}"
                    )
                    adjusted_weights[metric] = weight

            available_stats = [s for s in stat_columns if s not in current_individual_weights]
            if available_stats:
                st.markdown("---")
                st.markdown("**Add More Stats:**")
                additional_stats = st.multiselect(
                    "Select additional individual stats to include:",
                    options=available_stats,
                    default=[],
                    help="Add more stats to the similarity calculation"
                )

                for metric in additional_stats:
                    weight = st.slider(
                        metric,
                        min_value=0.0,
                        max_value=1.0,
                        value=0.1,
                        step=0.05,
                        key=f"sim_weight_ind_add_{metric}"
                    )
                    adjusted_weights[metric] = weight

            min_age = int(df_filtered['Age'].min())
            max_age = int(df_filtered['Age'].max())
            age_range = st.slider(
                "Age Range:",
                min_value=min_age,
                max_value=max_age,
                value=(22, 35),
                help="Filter by player age range",
                key="similarity_age_range"
            )

        with metric_tab2:
            st.markdown("#### Attributes")
            st.caption("💡 Note: These composite attributes are displayed in results but NOT used for similarity calculation.")
            st.caption("Similarity is based on Individual Statistics only.")

            st.markdown("##### Available Composite Attributes")

            # for attr_key, attr_config in COMPOSITE_ATTRIBUTES.items():
            #     comp_col = f"COMP_{attr_key}"
            #     display_name = f"{attr_config.get('icon', '')} {attr_config['display_name']}"
            #     description = attr_config.get('description', '')

            #     #with st.expander(f"{display_name}", expanded=False):
            #     st.write(f"**Description:** {description}")
            #     st.write("**Component Stats:**")
            #     for component in attr_config.get('components', []):
            #         stat_name = component['stat']
            #         weight = component['weight']
            #         st.write(f"- {stat_name} (weight: {weight:.2f})")

        st.session_state.similarity_weights = adjusted_weights

        if adjusted_weights:
            total_weight = sum(abs(w) for w in adjusted_weights.values())
            st.info(f"**Total Weight**: {total_weight:.2f} (will be normalized to 1.0)")

    st.markdown("---")

    # ========== ADDITIONAL FILTERS SECTION ==========
    st.markdown("### 🔧 Additional Filters")

    col1, col2 = st.columns([2, 1])

    with col1:
        contract_expired_filter = st.checkbox(
            "Show only expired contracts",
            value=False,
            help="Filter results to show only players with expired contracts",
            key="similarity_contract_filter"
        )

    min_minutes = 0

    # ========== ADDITIONAL FILTERS SECTION ==========
    # st.markdown("### 🔧 Additional Filters")

    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     # Minutes played filter
    #     if 'Minutes' in df_filtered.columns:
    #         min_minutes = st.number_input(
    #             "Minimum Minutes Played:",
    #             min_value=0,
    #             max_value=int(df_filtered['Minutes'].max()),
    #             value=0,
    #             step=100,
    #             help="Filter out players with fewer minutes",
    #             key="similarity_min_minutes"
    #         )
    #     else:
    #         min_minutes = 0

    # with col2:
    #     # Age range filter
    #     min_age = int(df_filtered['Age'].min())
    #     max_age = int(df_filtered['Age'].max())
    #     age_range = st.slider(
    #         "Age Range:",
    #         min_value=min_age,
    #         max_value=max_age,
    #         value=(min_age, max_age),
    #         help="Filter by player age range",
    #         key="similarity_age_range"
    #     )

    # st.markdown("---")

    # ========== CALCULATE BUTTON ==========
    # Button callback - ONLY stores to session state (no display inside)
    if st.button("🔄 Find Similar Players", type="primary", key="calculate_similarity"):
        if not adjusted_weights or sum(adjusted_weights.values()) == 0:
            st.error("❌ Please select at least one metric with weight > 0")
            st.session_state.similarity_results = None
        else:
            with st.spinner("Calculating player similarity..."):
                individual_weights = {
                    k: v for k, v in adjusted_weights.items()
                    if k in stat_columns and k in df_filtered.columns
                }

                if not individual_weights:
                    st.error("❌ Please select at least one individual statistic with weight > 0")
                    st.session_state.similarity_results = None
                    return

                scorer = SimilarityScorer(df_filtered, stat_columns, composite_columns)

                try:
                    results_df = scorer.calculate_similarity(
                        reference_player_name=selected_player,
                        weights=individual_weights,
                        min_minutes=min_minutes,
                        age_range=age_range,
                        same_position_only=False,
                        top_n=30,
                        contract_expired=contract_expired_filter
                    )

                    if len(results_df) == 0:
                        st.warning("⚠️ No similar players found with the current filters. Try adjusting your filters.")
                        st.session_state.similarity_results = None
                    else:
                        result_players = results_df['Player'].tolist()
                        result_players.append(selected_player)

                        composite_data = df_filtered[df_filtered['Player'].isin(result_players)][
                            ['Player'] + composite_columns
                        ]

                        results_df = results_df.merge(
                            composite_data,
                            on='Player',
                            how='left'
                        )

                        st.session_state.similarity_results = {
                            'results_df': results_df,
                            'scorer': scorer,
                            'reference_player': selected_player,
                            'weights': individual_weights,
                            'composite_display_names': composite_display_names,
                            'df_filtered': df_filtered,
                            'stat_columns': stat_columns,
                            'composite_columns': composite_columns,
                            'relevant_composites': [f"COMP_{attr}" for attr in relevant_composites]
                        }

                except Exception as e:
                    st.error(f"❌ Error calculating similarity: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())
                    st.session_state.similarity_results = None

    # ========== DISPLAY RESULTS (OUTSIDE BUTTON BLOCK) ==========
    # This section always displays results if they exist in session state
    # This prevents page reset when selectboxes in scatter plots change
    if 'similarity_results' in st.session_state and st.session_state.similarity_results is not None:
        results = st.session_state.similarity_results

        st.subheader("📊 Similarity Results")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📋 Results Table",
            "🎯 Attributes Scatter",
            "📊 Individual Stats Scatter",
            "🔍 Player Detail"
        ])

        with tab1:
            # Results table
            display_similarity_results_table(
                results['results_df'],
                results['reference_player'],
                results['weights'],
                results['composite_display_names'],
                results['relevant_composites']
            )

        with tab2:
            # Composite attributes scatter plot (moved up - now Tab 2)
            display_similarity_scatter_plot_composite(
                results['results_df'],
                results['df_filtered'],
                results['reference_player'],
                results['composite_columns'],
                results['composite_display_names'],
                results['weights']
            )

        with tab3:
            # Individual stats scatter plot visualization (moved down - now Tab 3)
            display_similarity_scatter_plot(
                results['results_df'],
                results['df_filtered'],
                results['reference_player'],
                results['stat_columns'],
                results['weights']
            )

        with tab4:
            # Player detail comparison
            display_similarity_player_detail(
                results['results_df'],
                results['scorer'],
                results['reference_player'],
                results['weights']
            )


def display_similarity_results_table(results_df, reference_player, weights, composite_display_names, relevant_composites):
    """Display top 30 similar players table with all composite attributes"""
    st.markdown("#### Top 30 Most Similar Players")

    display_df = results_df.copy()
    display_df['Similarity_Score'] = display_df['Similarity_Score'].round(3)
    display_df['Similarity_Percentile'] = display_df['Similarity_Percentile'].round(1)

    display_cols = ['Rank', 'Player', 'Team', 'Position', 'Age',
                   'contract_expiry', 'Similarity_Score', 'Similarity_Percentile']

    for metric in weights.keys():
        if metric in display_df.columns and metric not in display_cols:
            display_cols.append(metric)

    all_comp_cols = [col for col in display_df.columns if col.startswith('COMP_')]
    for comp_col in all_comp_cols:
        if comp_col not in display_cols:
            display_cols.append(comp_col)

    display_cols = [col for col in display_cols if col in display_df.columns]
    display_df = display_df[display_cols]

    rename_dict = {}
    for col in display_df.columns:
        if col.startswith('COMP_'):
            rename_dict[col] = composite_display_names.get(col, col)
    display_df = display_df.rename(columns=rename_dict)

    # Column configuration
    column_config = {
        'Rank': st.column_config.NumberColumn("#", width="small"),
        'contract_expiry': st.column_config.CheckboxColumn(
            "Contract Expired",
            help="Yes = contract has expired, No = contract is active",
            width="small"
        ),
        'Similarity_Score': st.column_config.NumberColumn(
            "Similarity Score",
            format="%.3f",
            width="medium",
            help="Cosine similarity score (higher = more similar)"
        ),
        'Similarity_Percentile': st.column_config.ProgressColumn(
            "Similarity %",
            min_value=0,
            max_value=100,
            format="%.0f%%",
            width="medium"
        )
    }

    for metric in weights.keys():
        if metric in display_df.columns:
            column_config[metric] = st.column_config.NumberColumn(
                metric,
                format="%.1f",
                width="small"
            )

    all_comp_cols = [col for col in display_df.columns if col.startswith('COMP_')]
    for comp_col in all_comp_cols:
        if comp_col in display_df.columns:
            display_name = composite_display_names.get(comp_col, comp_col)
            column_config[display_name] = st.column_config.NumberColumn(
                display_name,
                format="%.1f",
                width="medium"
            )

    st.dataframe(
        display_df,
        column_config=column_config,
        use_container_width=True,
        hide_index=True,
        height=600
    )

    # Summary stats
    st.markdown("##### 📊 Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Similar Players Found", len(display_df))
    with col2:
        st.metric("Highest Similarity", f"{display_df['Similarity_Score'].max():.3f}")
    with col3:
        st.metric("Average Similarity", f"{display_df['Similarity_Score'].mean():.3f}")
    with col4:
        st.metric("Teams Represented", display_df['Team'].nunique())

    st.markdown("##### ⚖️ Individual Statistics Weights Used")
    weights_df = pd.DataFrame([
        {'Metric': metric, 'Weight': f"{weight:.3f}"}
        for metric, weight in weights.items()
    ])
    st.dataframe(weights_df, use_container_width=True, hide_index=True)


def display_similarity_scatter_plot(results_df, full_df, reference_player, stat_columns, weights):
    """Display scatter plot of similar players"""
    import plotly.graph_objects as go

    st.markdown("#### Scatter Plot Analysis")

    # Metric selection for X/Y axes
    col1, col2 = st.columns(2)
    with col1:
        x_metric = st.selectbox(
            "X-Axis Metric:",
            options=stat_columns,
            index=0 if len(stat_columns) > 0 else None,
            key="scatter_x_metric"
        )
    with col2:
        y_metric = st.selectbox(
            "Y-Axis Metric:",
            options=stat_columns,
            index=1 if len(stat_columns) > 1 else 0,
            key="scatter_y_metric"
        )

    if not x_metric or not y_metric:
        st.warning("Please select both X and Y metrics")
        return

    # Create scatter plot
    fig = go.Figure()

    # Background players (not in results, not reference)
    similar_names = set(results_df['Player'].tolist())
    similar_names.add(reference_player)
    background_df = full_df[~full_df['Player'].isin(similar_names)]

    if len(background_df) > 0 and x_metric in background_df.columns and y_metric in background_df.columns:
        fig.add_trace(go.Scatter(
            x=background_df[x_metric],
            y=background_df[y_metric],
            mode='markers',
            marker=dict(color='#9E9E9E', size=10, opacity=0.3),
            name='Other Players',
            text=background_df['Player'],
            hovertemplate='<b>%{text}</b><br>' +
                         f'{x_metric}: %{{x:.1f}}<br>' +
                         f'{y_metric}: %{{y:.1f}}<extra></extra>'
        ))

    # Similar players
    if x_metric in results_df.columns and y_metric in results_df.columns:
        # Create hover text with similarity scores
        hover_texts = []
        for idx, row in results_df.iterrows():
            hover_texts.append(
                f"<b>{row['Player']}</b><br>" +
                f"{x_metric}: {row[x_metric]:.1f}<br>" +
                f"{y_metric}: {row[y_metric]:.1f}<br>" +
                f"Similarity: {row['Similarity_Score']:.3f}"
            )

        fig.add_trace(go.Scatter(
            x=results_df[x_metric],
            y=results_df[y_metric],
            mode='markers+text',
            marker=dict(color='#2ecc71', size=12, opacity=0.8),
            name='Similar Players',
            text=results_df['Player'],
            textposition='top center',
            textfont=dict(size=9),
            hovertemplate='%{hovertext}<extra></extra>',
            hovertext=hover_texts
        ))

    # Reference player
    ref_player_row = full_df[full_df['Player'] == reference_player].iloc[0]
    if x_metric in ref_player_row and y_metric in ref_player_row:
        fig.add_trace(go.Scatter(
            x=[ref_player_row[x_metric]],
            y=[ref_player_row[y_metric]],
            mode='markers+text',
            marker=dict(color='#e74c3c', size=15, symbol='star',
                       line=dict(width=2, color='white')),
            name='Reference Player',
            text=[reference_player],
            textposition='top center',
            textfont=dict(size=11, color='#e74c3c'),
            hovertemplate=f'<b>{reference_player}</b><br>' +
                         f'{x_metric}: {ref_player_row[x_metric]:.1f}<br>' +
                         f'{y_metric}: {ref_player_row[y_metric]:.1f}<extra></extra>'
        ))

    # Update layout
    fig.update_layout(
        title=f"{x_metric} vs {y_metric} - Similarity Analysis",
        xaxis_title=x_metric,
        yaxis_title=y_metric,
        height=600,
        plot_bgcolor='#f5f3e8',
        paper_bgcolor='#f5f3e8',
        hovermode='closest'
    )

    st.plotly_chart(fig, use_container_width=True)


def display_similarity_scatter_plot_composite(results_df, full_df, reference_player,
                                            composite_columns, composite_display_names, weights):
    """Display scatter plot with composite attributes on axes"""
    import plotly.graph_objects as go

    st.markdown("#### Attributes Scatter Plot")

    # Metric selection for X/Y axes - only composite attributes
    col1, col2 = st.columns(2)

    # Create friendly display options
    composite_options_display = [composite_display_names[col] for col in composite_columns if col in full_df.columns]
    composite_options_mapping = {display: col for display, col in zip(composite_options_display, [col for col in composite_columns if col in full_df.columns])}

    if len(composite_options_display) < 2:
        st.warning("Not enough composite attributes available. Please ensure data is loaded correctly.")
        return

    with col1:
        x_metric_display = st.selectbox(
            "X-Axis Composite Attribute:",
            options=composite_options_display,
            index=0,
            key="scatter_comp_x_metric"
        )
        x_metric = composite_options_mapping.get(x_metric_display)

    with col2:
        y_metric_display = st.selectbox(
            "Y-Axis Composite Attribute:",
            options=composite_options_display,
            index=1 if len(composite_options_display) > 1 else 0,
            key="scatter_comp_y_metric"
        )
        y_metric = composite_options_mapping.get(y_metric_display)

    if not x_metric or not y_metric:
        st.warning("Please select both X and Y composite attributes")
        return

    # Create scatter plot
    fig = go.Figure()

    # Background players (not in results, not reference)
    similar_names = set(results_df['Player'].tolist())
    similar_names.add(reference_player)
    background_df = full_df[~full_df['Player'].isin(similar_names)]

    if len(background_df) > 0 and x_metric in background_df.columns and y_metric in background_df.columns:
        fig.add_trace(go.Scatter(
            x=background_df[x_metric],
            y=background_df[y_metric],
            mode='markers',
            marker=dict(color='#9E9E9E', size=10, opacity=0.3),
            name='Other Players',
            text=background_df['Player'],
            hovertemplate='<b>%{text}</b><br>' +
                         f'{x_metric_display}: %{{x:.1f}}<br>' +
                         f'{y_metric_display}: %{{y:.1f}}<extra></extra>'
        ))

    # Similar players
    if x_metric in results_df.columns and y_metric in results_df.columns:
        hover_texts = []
        for idx, row in results_df.iterrows():
            hover_texts.append(
                f"<b>{row['Player']}</b><br>" +
                f"{x_metric_display}: {row[x_metric]:.1f}<br>" +
                f"{y_metric_display}: {row[y_metric]:.1f}<br>" +
                f"Similarity: {row['Similarity_Score']:.3f}"
            )

        fig.add_trace(go.Scatter(
            x=results_df[x_metric],
            y=results_df[y_metric],
            mode='markers+text',
            marker=dict(color='#2ecc71', size=12, opacity=0.8),
            name='Similar Players',
            text=results_df['Player'],
            textposition='top center',
            textfont=dict(size=9),
            hovertemplate='%{hovertext}<extra></extra>',
            hovertext=hover_texts
        ))

    # Reference player
    ref_player_row = full_df[full_df['Player'] == reference_player]
    if len(ref_player_row) > 0:
        ref_player_row = ref_player_row.iloc[0]
        fig.add_trace(go.Scatter(
            x=[ref_player_row[x_metric]],
            y=[ref_player_row[y_metric]],
            mode='markers+text',
            marker=dict(color='#e74c3c', size=15, symbol='star',
                       line=dict(width=2, color='white')),
            name='Reference Player',
            text=[reference_player],
            textposition='top center',
            textfont=dict(size=11, color='#e74c3c'),
            hovertemplate=f'<b>{reference_player}</b><br>' +
                         f'{x_metric_display}: {ref_player_row[x_metric]:.1f}<br>' +
                         f'{y_metric_display}: {ref_player_row[y_metric]:.1f}<extra></extra>'
        ))

    # Update layout
    fig.update_layout(
        title=f"{x_metric_display} vs {y_metric_display} - Attributes Analysis",
        xaxis_title=x_metric_display,
        yaxis_title=y_metric_display,
        height=600,
        plot_bgcolor='#f5f3e8',
        paper_bgcolor='#f5f3e8',
        hovermode='closest'
    )

    st.plotly_chart(fig, use_container_width=True)

    # Add explanation
    from config.composite_attributes import COMPOSITE_ATTRIBUTES
    x_attr_key = x_metric.replace("COMP_", "")
    y_attr_key = y_metric.replace("COMP_", "")

    st.info(
        "💡 **How to interpret this chart:**\n\n"
        f"- **X-Axis ({x_metric_display})**: {COMPOSITE_ATTRIBUTES[x_attr_key]['description']}\n\n"
        f"- **Y-Axis ({y_metric_display})**: {COMPOSITE_ATTRIBUTES[y_attr_key]['description']}\n\n"
        "- Players closer to the reference player (red star) are more similar across these composite attributes"
    )


def display_similarity_player_detail(results_df, scorer, reference_player, weights):
    """Display detailed player comparison with both composite and individual contributions"""
    import plotly.express as px
    from config.composite_attributes import COMPOSITE_ATTRIBUTES

    st.markdown("#### Individual Player Comparison")

    # Player selection
    selected_similar_player = st.selectbox(
        "Select a similar player to compare:",
        options=results_df['Player'].tolist(),
        key="detail_similar_player"
    )

    if not selected_similar_player:
        st.info("Select a player to view detailed comparison")
        return

    individual_contributions = scorer.get_metric_contributions(
        reference_player,
        selected_similar_player,
        weights
    )

    st.markdown(f"##### Comparing: **{reference_player}** vs **{selected_similar_player}**")

    # ========== Individual Metric Contributions ==========
    if individual_contributions:
        st.markdown("---")
        st.markdown("#### 📊 Individual Metric Contributions")
        st.caption("Raw statistical attributes used in similarity calculation")

        # Create comparison table
        comparison_data = []
        for metric, data in sorted(
            individual_contributions.items(),
            key=lambda x: x[1]['weighted_contribution'],
            reverse=True
        ):
            comparison_data.append({
                'Metric': metric,
                f'{reference_player}': f"{data['reference_value']:.1f}",
                f'{selected_similar_player}': f"{data['similar_value']:.1f}",
                'Difference': f"{data['difference']:.1f}",
                'Similarity %': f"{data['metric_similarity']:.1f}%",
                'Weight': f"{data['weight']:.2f}",
                'Contribution': f"{data['weighted_contribution']:.1f}"
            })

        comparison_df = pd.DataFrame(comparison_data)
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)

        # Visualization of contributions
        contribution_values = [float(row['Contribution']) for _, row in comparison_df.iterrows()]
        similarity_values = [float(row['Similarity %'].replace('%', '')) for _, row in comparison_df.iterrows()]

        fig = px.bar(
            comparison_df,
            x='Metric',
            y=contribution_values,
            title=f"Individual Metric Contributions to Similarity Score",
            color=similarity_values,
            color_continuous_scale='RdYlGn',
            labels={'y': 'Weighted Contribution', 'color': 'Similarity %'}
        )
        fig.update_layout(
            height=400,
            plot_bgcolor='#f5f3e8',
            paper_bgcolor='#f5f3e8',
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

    # ========== ALL COMPOSITE ATTRIBUTES (Display Only) ==========
    st.markdown("---")
    st.markdown("#### 🎯 All Composite Attribute Contributions")
    st.caption("Composite attributes for comparison (not used in similarity calculation)")

    all_composite_contributions = scorer.get_all_composite_contributions(
        reference_player,
        selected_similar_player,
        COMPOSITE_ATTRIBUTES
    )

    if all_composite_contributions:
        comp_data = []
        for comp_col, data in sorted(
            all_composite_contributions.items(),
            key=lambda x: x[1]['metric_similarity'],
            reverse=True
        ):
            comp_data.append({
                'Attribute': data['display_name'],
                f"{reference_player}": f"{data['reference_value']:.1f}",
                f"{selected_similar_player}": f"{data['similar_value']:.1f}",
                'Difference': f"{data['difference']:.1f}",
                'Similarity %': f"{data['metric_similarity']:.1f}%"
            })

        comp_df = pd.DataFrame(comp_data)
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

def main():
    # Title and description
    st.title("Scouting Hub.")
#    st.markdown("### Player Comparison & Defender Finder (darfat)")
#    st.markdown("Compare players side-by-side and find top defenders using weighted scoring profiles.")

    # Load global data (cached)
    with st.spinner("Loading player data from all leagues..."):
        df_global = load_global_data()

    # Extract distinct values for filters
    distinct_values = get_distinct_values(df_global)

    # ========== SIDEBAR: GLOBAL FILTERS (TOP) ==========
    st.sidebar.markdown("### 🔍 Global Filters")
    st.sidebar.markdown("*Apply to all pages*")

    # League filter
    selected_leagues = st.sidebar.multiselect(
        "Select Leagues:",
        options=["All Leagues"] + distinct_values['leagues'],
        default=["All Leagues"],
        help="Filter by leagues across all pages",
        key="global_league_filter"
    )
    league_filter = None if "All Leagues" in selected_leagues or len(selected_leagues) == 0 else selected_leagues

    # Position group filter (radio buttons for single-select)
    selected_position_group = st.sidebar.radio(
        "Select Position Group:",
        options=get_position_group_options(),
        index=0,  # Default to "All"
        help="Filter by predefined position groups. Select one group at a time.",
        key="global_position_group_filter"
    )

    # Convert selected group to position list for filter_players()
    position_filter = POSITION_GROUPS.get(selected_position_group, None)

    # Contract expired filter
    contract_expired_filter = st.sidebar.checkbox(
        "Contract Expired",
        value=False,
        help="Show only players with expired contracts",
        key="global_contract_expiry_filter"
    )

    # Apply global filters
    df_filtered = filter_players(df_global, positions=position_filter, leagues=league_filter, contract_expired=contract_expired_filter)

    # Filter summary
    st.sidebar.info(f"📊 Showing **{len(df_filtered)}** players (from {len(df_global)} total)")

    # Check for empty results
    if len(df_filtered) == 0:
        st.sidebar.warning("⚠️ No players match filters")

    st.sidebar.markdown("---")

    # ========== SIDEBAR: NAVIGATION ==========
    st.sidebar.markdown("### 🧭 Navigation")
    page = st.sidebar.radio(
        "Select Page:",
        options=["⚽ Player Comparison", "🎯 Player Finder", "🔍 Player Similarity"],
        key="page_navigation",
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    # ========== MAIN CONTENT ==========
    st.markdown("---")

    if page == "⚽ Player Comparison":
        render_player_comparison_page(df_filtered)
    elif page == "🎯 Player Finder":
        render_player_finder_page(df_filtered)
    elif page == "🔍 Player Similarity":
        render_player_similarity_page(df_filtered)

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #7f8c8d; font-size: 12px;">
        Data source: Wyscout | Multiple Leagues 2025-2026<br>
        All statistics are shown as percentile ranks (0-100) calculated globally across {len(df_global)} players from all leagues
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
