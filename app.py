"""
Streamlit app for football player comparison
Eliteserien 2025 - DM/CM Players
"""
import streamlit as st
import os
from config.stat_categories import STAT_CATEGORIES, PLAYER_INFO_COLUMNS, PLAYER_COLORS
from config.composite_attributes import COMPOSITE_ATTRIBUTES
from utils.data_loader import prepare_data_global, get_player_info, get_player_stats, get_all_stat_columns, calculate_composite_attributes, get_distinct_values, filter_players
from utils.visualizations import display_player_comparison, create_stats_table, display_composite_attributes, display_position_based_rankings


# Page configuration
st.set_page_config(
    page_title="Player Comparison - Eliteserien 2025",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f5f3e8;
    }
    .stSelectbox {
        background-color: white;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
    }
    h2, h3 {
        color: #34495e;
    }
</style>
""", unsafe_allow_html=True)


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


def main():
    # Title and description
    st.title("⚽ Football Player Comparison")
    st.markdown("### Player Scouting Tool (darfat)")
    st.markdown("Compare up to 3 players across defensive, progressive, and offensive statistics from multiple leagues.")

    # Load global data (cached)
    with st.spinner("Loading player data from all leagues..."):
        df_global = load_global_data()

    # Extract distinct values for filters
    distinct_values = get_distinct_values(df_global)

    # === FILTERS IN MAIN AREA ===
    st.markdown("---")
    st.markdown("#### 🔍 Filter Players")

    col_filter1, col_filter2 = st.columns(2)

    with col_filter1:
        # Position multi-select filter
        selected_positions = st.multiselect(
            "Select Positions:",
            options=["All Positions"] + distinct_values['positions'],
            default=["All Positions"],
            help="Filter by player positions. Select 'All Positions' to see everyone.",
            key="position_filter"
        )

        # Handle "All Positions" selection
        if "All Positions" in selected_positions or len(selected_positions) == 0:
            position_filter = None  # No filtering
        else:
            position_filter = selected_positions

    with col_filter2:
        # League multi-select filter
        selected_leagues = st.multiselect(
            "Select Leagues:",
            options=["All Leagues"] + distinct_values['leagues'],
            default=["All Leagues"],
            help="Filter by leagues. Select 'All Leagues' to see all.",
            key="league_filter"
        )

        # Handle "All Leagues" selection
        if "All Leagues" in selected_leagues or len(selected_leagues) == 0:
            league_filter = None  # No filtering
        else:
            league_filter = selected_leagues

    # Apply filters to get filtered dataframe
    df = filter_players(df_global, positions=position_filter, leagues=league_filter)

    # Check for empty filter results
    if len(df) == 0:
        st.warning("⚠️ No players match the selected filters. Please adjust your position/league filters.")
        return

    # Display filter summary
    st.markdown(f"**Showing {len(df)} players** (filtered from {len(df_global)} total)")

    st.markdown("---")

    # Get list of players from FILTERED dataframe
    player_names = sorted(df[PLAYER_INFO_COLUMNS['name']].tolist())

    # Sidebar for player selection
    st.sidebar.header("Player Selection")
    st.sidebar.markdown(f"Select 2-3 players from {len(player_names)} available")

    selected_players = st.sidebar.multiselect(
        "Choose players:",
        options=player_names,
        max_selections=3,
        help="Select between 2 and 3 players to compare"
    )

    # Show instructions if no players selected
    if len(selected_players) == 0:
        st.info("👈 Please select at least 2 players from the sidebar to begin comparison.")

        # Show stats about the FILTERED dataset
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Filtered Players", len(df))
        with col2:
            avg_age = df[PLAYER_INFO_COLUMNS['age']].mean()
            st.metric("Average Age", f"{avg_age:.1f}")
        with col3:
            num_teams = df[PLAYER_INFO_COLUMNS['team']].nunique()
            st.metric("Teams", num_teams)

        st.markdown("---")
        st.markdown("#### Available Players")
        st.dataframe(
            df[[
                PLAYER_INFO_COLUMNS['name'],
                PLAYER_INFO_COLUMNS['age'],
                PLAYER_INFO_COLUMNS['team'],
                PLAYER_INFO_COLUMNS['position'],
                PLAYER_INFO_COLUMNS['country']
            ]].sort_values(PLAYER_INFO_COLUMNS['name']),
            use_container_width=True,
            hide_index=True
        )
        return

    # Validate selection
    if len(selected_players) < 2:
        st.warning("⚠️ Please select at least 2 players to compare.")
        return

    # Prepare player data
    players_data = []
    stat_columns = get_all_stat_columns(STAT_CATEGORIES)

    for player_name in selected_players:
        player_info = get_player_info(df, player_name, PLAYER_INFO_COLUMNS)
        player_stats = get_player_stats(df, player_name, stat_columns)

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
    # Map player positions to position categories
    first_player_position = players_data[0]['info']['position']

    # Simple position mapping - can be enhanced later
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

    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #7f8c8d; font-size: 12px;">
        Data source: Wyscout | Multiple Leagues 2025-2026<br>
        All statistics are shown as percentile ranks (0-100) calculated globally across {len(df_global)} players from all leagues<br>
        Currently viewing {len(df)} players (after filters)
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
