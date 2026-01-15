"""
Visualization utilities for player comparison charts
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from typing import List, Dict
import streamlit as st
import pandas as pd
import numpy as np


def get_percentile_color(percentile: float) -> str:
    """
    Get color based on percentile rank

    Args:
        percentile: Percentile value (0-100)

    Returns:
        Hex color string
    """
    if percentile >= 80:
        return '#2ecc71'  # Green - Excellent
    elif percentile >= 60:
        return '#3498db'  # Blue - Good
    elif percentile >= 40:
        return '#f39c12'  # Orange - Average
    else:
        return '#e74c3c'  # Red - Below Average


def create_combined_player_chart(
    player_data: Dict,
    stat_categories: Dict,
    player_color: str
):
    """
    Create combined player performance chart with all categories

    Args:
        player_data: Dictionary containing player stats
        stat_categories: Dictionary of all stat categories
        player_color: Primary color for the player

    Returns:
        matplotlib figure
    """
    # Collect all stats from all categories
    all_percentiles = []
    all_colors = []
    all_labels = []
    category_positions = []
    category_names = []

    current_position = 0

    # Process each category in order: Defensive, Progressive, Offensive, General
    for category_key in ['Defensive', 'Progressive', 'Offensive', 'General']:
        if category_key not in stat_categories:
            continue

        category_config = stat_categories[category_key]
        category_stats = category_config['stats']

        # Mark the start position and name of this category
        category_positions.append(current_position + len(category_stats) / 2)
        category_names.append(category_key.upper())

        # Add stats from this category
        for stat in category_stats:
            stat_col = stat['column']
            percentile = player_data['stats'].get(stat_col, {}).get('percentile', 0)
            all_percentiles.append(percentile)
            all_colors.append(get_percentile_color(percentile))
            all_labels.append(stat['display'])
            current_position += 1

    total_stats = len(all_percentiles)

    # Create figure with extra space on left for category labels
    fig, ax = plt.subplots(figsize=(8, total_stats * 0.35 + 1))

    # Set background color
    fig.patch.set_facecolor('#f5f3e8')
    ax.set_facecolor('#f5f3e8')

    # Create horizontal bars
    y_positions = range(total_stats)
    bars = ax.barh(
        y_positions,
        all_percentiles,
        color=all_colors,
        alpha=0.85,
        edgecolor='white',
        linewidth=1.5
    )

    # Add percentile text on bars
    for i, (bar, percentile) in enumerate(zip(bars, all_percentiles)):
        width = bar.get_width()
        ax.text(
            width + 2,
            bar.get_y() + bar.get_height() / 2,
            f'{percentile:.0f}',
            va='center',
            fontsize=8,
            fontweight='bold',
            color='#2c3e50'
        )

    # Add separator lines between categories
    separator_positions = []
    current_pos = 0
    for category_key in ['Defensive', 'Progressive', 'Offensive', 'General']:
        if category_key not in stat_categories:
            continue
        num_stats = len(stat_categories[category_key]['stats'])
        current_pos += num_stats
        if current_pos < total_stats:  # Don't add line after last category
            separator_positions.append(current_pos - 0.5)

    for sep_pos in separator_positions:
        ax.axhline(y=sep_pos, color='#95a5a6', linestyle='--', linewidth=1.5, alpha=0.5)

    # Customize axes
    ax.set_yticks(y_positions)
    ax.set_yticklabels(all_labels, fontsize=9)
    ax.set_xlabel('Percentile Rank', fontsize=10, fontweight='bold', color='#2c3e50')
    ax.set_xlim(0, 105)
    ax.set_xticks([0, 25, 50, 75, 100])

    # Add grid
    ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#95a5a6')
    ax.spines['bottom'].set_color('#95a5a6')

    # Invert y-axis to have first stat on top
    ax.invert_yaxis()

    # Add vertical category labels on the left
    # Adjust the position to be in the left margin
    fig.subplots_adjust(left=0.35)

    for cat_pos, cat_name in zip(category_positions, category_names):
        ax.text(
            110,  # Position in the left margin
            cat_pos,
            cat_name,
            rotation=90,
            va='center',
            ha='center',
            fontsize=11,
            fontweight='bold',
            color='#34495e',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#ecf0f1', edgecolor='#95a5a6', linewidth=1)
        )

    # Adjust layout
    plt.tight_layout()

    return fig


def create_player_header(player_info: Dict, color: str):
    """
    Create a styled player information header

    Args:
        player_info: Dictionary with player information
        color: Color for the header accent

    Returns:
        HTML string for player header
    """
    header_html = f"""
    <div style="
        background: linear-gradient(135deg, {color}15 0%, {color}05 100%);
        border-left: 5px solid {color};
        border-radius: 8px;
        padding: 20px 15px;
        margin: 10px 0 20px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    ">
        <h2 style="margin: 0 0 4px 0; color: #2c3e50; font-size: 22px; font-weight: 700;">
            {player_info['name']}
        </h2>
        <div style="margin: 0; color: #7f8c8d; font-size: 13px; line-height: 1.6;">
            <strong>Age:</strong> {player_info['age']} |
            <strong>Position:</strong> {player_info['position']}<br>
            <strong>Team:</strong> {player_info['team']} |
            <strong>Country:</strong> {player_info['country']} | <strong>Min Played:</strong> {player_info['minutes']}
        </div>
    </div>
    """
    return header_html


def display_player_comparison(
    players_data: List[Dict],
    stat_categories: Dict,
    player_colors: List[str]
):
    """
    Display complete player comparison with side-by-side column layout

    Args:
        players_data: List of player data dictionaries
        stat_categories: Dictionary of stat categories
        player_colors: List of colors for players
    """
    num_players = len(players_data)

    # Create columns for each player
    st.markdown("### Player Comparison")

    # Create columns for player headers and combined charts
    cols = st.columns(num_players)

    for idx, (col, player_data) in enumerate(zip(cols, players_data)):
        with col:
            # Display player header
            st.markdown(
                create_player_header(player_data['info'], player_colors[idx]),
                unsafe_allow_html=True
            )

            # Display combined chart with all categories
            fig = create_combined_player_chart(
                player_data,
                stat_categories,
                player_colors[idx]
            )

            st.pyplot(fig, use_container_width=True)
            plt.close(fig)


def create_stats_table(players_data: List[Dict], stat_categories: Dict):
    """
    Create a detailed statistics table for selected players

    Args:
        players_data: List of player data dictionaries
        stat_categories: Dictionary of stat categories
    """
    import pandas as pd

    for category_key, category_config in stat_categories.items():
        st.markdown(f"#### {category_config['display_name']} - Detailed Stats")

        # Prepare data for table
        table_data = []
        for stat in category_config['stats']:
            row = {'Statistic': stat['display']}
            for player_data in players_data:
                stat_col = stat['column']
                value = player_data['stats'].get(stat_col, {}).get('value', 0)
                percentile = player_data['stats'].get(stat_col, {}).get('percentile', 0)
                row[player_data['info']['name']] = f"{value:.2f} ({percentile:.0f}%)"
            table_data.append(row)

        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)


def display_composite_attributes(
    players_data: List[Dict],
    player_colors: List[str]
):
    """
    Display composite attributes comparison for selected players

    Args:
        players_data: List of player data dictionaries (with 'composite_attributes' key)
        player_colors: List of colors for players
    """
    import pandas as pd
    import numpy as np

    st.markdown("---")
    st.markdown("### 📊 Attributes Analysis")
    st.markdown("*Calculated from weighted combinations of key statistics*")

    # Get all attribute names from the first player
    if not players_data or 'composite_attributes' not in players_data[0]:
        st.warning("Composite attributes not calculated for players.")
        return

    attribute_names = list(players_data[0]['composite_attributes'].keys())

    # Create a chart for each attribute showing all players
    for attr_key in attribute_names:
        attr_data = players_data[0]['composite_attributes'][attr_key]
        attr_name = attr_data['display_name']
        attr_icon = attr_data.get('icon', '')
        attr_desc = attr_data.get('description', '')

        # Collect scores for all players
        player_scores = []
        for player_data in players_data:
            score = player_data['composite_attributes'][attr_key]['score']
            player_scores.append({
                'name': player_data['info']['name'],
                'score': score
            })

        # Sort by score descending
        player_scores.sort(key=lambda x: x['score'], reverse=True)

        # Create horizontal bar chart
        fig, ax = plt.subplots(figsize=(10, max(2, len(players_data) * 0.6)))
        fig.patch.set_facecolor('#f5f3e8')
        ax.set_facecolor('#f5f3e8')

        # Prepare data
        names = [p['name'] for p in player_scores]
        scores = [p['score'] for p in player_scores]

        # Assign colors based on original player order
        bar_colors = []
        for player_score in player_scores:
            # Find this player's index in original players_data
            for idx, player_data in enumerate(players_data):
                if player_data['info']['name'] == player_score['name']:
                    bar_colors.append(player_colors[idx])
                    break

        y_positions = range(len(names))
        bars = ax.barh(
            y_positions,
            scores,
            color=bar_colors,
            alpha=0.85,
            edgecolor='white',
            linewidth=2
        )

        # Add score labels on bars
        for i, (bar, score) in enumerate(zip(bars, scores)):
            width = bar.get_width()
            ax.text(
                width + 1,
                bar.get_y() + bar.get_height() / 2,
                f'{score:.1f}',
                va='center',
                fontsize=11,
                fontweight='bold',
                color='#2c3e50'
            )

        # Add rank numbers
        for i, (bar, rank) in enumerate(zip(bars, range(1, len(names) + 1))):
            ax.text(
                -2,
                bar.get_y() + bar.get_height() / 2,
                f'#{rank}',
                va='center',
                ha='right',
                fontsize=10,
                fontweight='bold',
                color='#7f8c8d'
            )

        # Customize axes
        ax.set_yticks(y_positions)
        ax.set_yticklabels(names, fontsize=11, fontweight='bold')
        ax.set_xlabel('Score', fontsize=10, fontweight='bold', color='#2c3e50')
        ax.set_title(
            f'{attr_name}\n{attr_desc}',
            fontsize=10,
            fontweight='bold',
            color='#2c3e50',
            pad=0
        )

        # Set x-axis limits
        max_score = max(scores) if scores else 100
        ax.set_xlim(0, max_score)

        # Add grid
        ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
        ax.set_axisbelow(True)

        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#95a5a6')

        # Invert y-axis to show highest score on top
        ax.invert_yaxis()

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


def display_position_based_rankings(
    players_data: List[Dict],
    position_type: str,
    player_colors: List[str]
):
    """
    Display position-specific rankings for key composite attributes

    Args:
        players_data: List of player data dictionaries (with 'composite_attributes' key)
        position_type: Position type ("DM/CM" or "CB")
        player_colors: List of colors for players
    """
    from config.position_rankings import POSITION_RANKINGS

    if position_type not in POSITION_RANKINGS:
        return

    position_config = POSITION_RANKINGS[position_type]
    key_attributes = position_config['key_attributes']

    st.markdown("---")
    st.markdown("### 🏆 Position-Based Rankings")
    st.markdown(f"*Key attributes for {position_config['display_name']}*")

    # Medal icons for top 3
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}

    # Create ranking data for each key attribute
    ranking_data = []

    for attr_key in key_attributes:
        # Collect scores for all players for this attribute
        player_scores = []
        for idx, player_data in enumerate(players_data):
            if 'composite_attributes' not in player_data:
                continue

            if attr_key not in player_data['composite_attributes']:
                continue

            score = player_data['composite_attributes'][attr_key]['score']
            player_scores.append({
                'name': player_data['info']['name'],
                'score': score,
                'color': player_colors[idx]
            })

        # Sort by score descending
        player_scores.sort(key=lambda x: x['score'], reverse=True)

        # Build ranking string
        ranking_parts = []
        for rank, player in enumerate(player_scores[:3], 1):  # Top 3 only
            medal = medals.get(rank, "")
            ranking_parts.append(f"{medal} #{rank} {player['name']} ({player['score']:.1f})")

        ranking_string = " • ".join(ranking_parts) if ranking_parts else "N/A"

        # Get attribute display info
        attr_info = players_data[0]['composite_attributes'].get(attr_key, {})
        attr_icon = attr_info.get('icon', '')
        attr_display = attr_info.get('display_name', attr_key)

        ranking_data.append({
            'Attribute': f"{attr_icon} {attr_display}",
            'Rankings': ranking_string
        })

    # Display as a styled dataframe
    import pandas as pd
    df_rankings = pd.DataFrame(ranking_data)

    # Custom CSS for the table
    st.markdown("""
    <style>
    .rankings-table {
        font-size: 14px;
        line-height: 1.8;
    }
    </style>
    """, unsafe_allow_html=True)

    st.dataframe(
        df_rankings,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Attribute": st.column_config.TextColumn(
                "Attribute",
                width="medium",
            ),
            "Rankings": st.column_config.TextColumn(
                "Top Players",
                width="large",
            )
        }
    )


def display_attribute_rankings_1d_dot(
    players_data: List[Dict],
    df_filtered: pd.DataFrame,
    position_type: str,
    player_colors: List[str]
):
    """
    Display attribute rankings for selected players using 1D dot chart

    Shows all players as background gray dots with selected players highlighted
    in their respective colors with labels. Shows rank for relevant composite attributes
    based on position type.

    Args:
        players_data: List of selected player data dictionaries (with 'composite_attributes' key)
        df_filtered: Filtered DataFrame with all players
        position_type: Position type ("CB", "DM/CM", "FB/WB", "CF", "Winger", "AM")
        player_colors: List of colors for selected players
    """
    from config.position_rankings import POSITION_RANKINGS
    from config.composite_attributes import COMPOSITE_ATTRIBUTES

    st.markdown("---")
    st.markdown("### Responsibility Rankings - Distribution")
    st.markdown("*Shows where selected players rank among all players in filtered dataset*")

    if position_type not in POSITION_RANKINGS:
        st.warning(f"Position type '{position_type}' not found in rankings configuration.")
        return

    position_config = POSITION_RANKINGS[position_type]
    relevant_attributes = position_config['key_attributes']

    selected_player_names = [p['info']['name'] for p in players_data]

    fig, ax = plt.subplots(figsize=(14, len(relevant_attributes) * 1.2 + 1))
    fig.patch.set_facecolor('#f5f3e8')
    ax.set_facecolor('#f5f3e8')

    y_positions = []
    attribute_names = []
    attr_display_info = []
    df_attr = None
    max_rank = 100

    for attr_key in relevant_attributes:
        if attr_key not in COMPOSITE_ATTRIBUTES:
            continue

        attr_config = COMPOSITE_ATTRIBUTES[attr_key]
        attr_display = f"{attr_config['display_name']}"
        attribute_names.append(attr_display)
        attr_display_info.append(attr_key)

        comp_col = f"COMP_{attr_key}"

        if comp_col not in df_filtered.columns:
            continue

        y_pos = len(y_positions)
        y_positions.append(y_pos)

        if comp_col not in df_filtered.columns:
            continue

        df_attr = df_filtered[[comp_col, 'Player']].copy()
        df_attr = df_attr.dropna()

        df_attr['rank'] = df_attr[comp_col].rank(method='min', ascending=False)
        max_rank = max(max_rank, df_attr['rank'].max())

        for _, row in df_attr.iterrows():
            player_name = row['Player']
            rank = row['rank']

            jitter = np.random.uniform(-0.15, 0.15)

            if player_name in selected_player_names:
                player_idx = selected_player_names.index(player_name)
                color = player_colors[player_idx]

                ax.scatter(
                    rank,
                    y_pos + jitter,
                    color=color,
                    s=150,
                    alpha=1.0,
                    edgecolor='white',
                    linewidth=2,
                    zorder=10
                )

                ax.annotate(
                    player_name,
                    (rank, y_pos + jitter),
                    xytext=(5, 0),
                    textcoords='offset points',
                    fontsize=5,
                    fontweight='bold',
                    color='#2c3e50',
                    va='center',
                    ha='left',
                    # bbox=dict(
                    #     boxstyle='round,pad=0.3',
                    #     facecolor=color + '40',
                    #     edgecolor=color,
                    #     linewidth=1
                    # )
                )
            else:
                ax.scatter(
                    rank,
                    y_pos + jitter,
                    color='#95a5a6',
                    s=20,
                    alpha=0.3,
                    edgecolor='none',
                    zorder=1
                )

    if not y_positions:
        st.warning("No composite attributes found for the selected position type.")
        plt.close(fig)
        return

    ax.set_yticks(y_positions)
    ax.set_yticklabels(attribute_names, fontsize=11, fontweight='bold')
    ax.set_xlabel('Rank Position', fontsize=12, fontweight='bold', color='#2c3e50')

    ax.set_xlim(max_rank, 0)

    ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_axisbelow(True)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#95a5a6')

    percentile_positions = [
        {'pct': 0.90, 'color': '#2ecc71', 'label': 'Top 10%'},
        {'pct': 0.75, 'color': '#3498db', 'label': 'Top 25%'},
        {'pct': 0.50, 'color': '#f39c12', 'label': 'Top 50%'}
    ]

    for pct_info in percentile_positions:
        x_pos = max_rank * (1 - pct_info['pct'])
        ax.axvline(x=x_pos, color=pct_info['color'], linestyle='--', linewidth=1.5, alpha=0.5)
        ax.text(
            x_pos,
            len(y_positions) - 0.5,
            pct_info['label'],
            fontsize=8,
            color=pct_info['color'],
            rotation=0,
            ha='center',
            va='bottom',
            alpha=0.7
        )

    legend_elements = []
    for idx, name in enumerate(selected_player_names):
        legend_elements.append(
            Line2D(
                [0], [0],
                marker='o',
                color='w',
                markerfacecolor=player_colors[idx],
                markersize=10,
                label=name,
                markeredgecolor='white',
                markeredgewidth=2
            )
        )

    legend_elements.append(
        Line2D(
            [0], [0],
            marker='o',
            color='w',
            markerfacecolor='#95a5a6',
            markersize=6,
            label='Other Players',
            alpha=0.5
        )
    )

    ax.legend(
        handles=legend_elements,
        loc='lower left',
        fontsize=8,
        framealpha=0.85,
        edgecolor='#95a5a6',
        facecolor='#ffffff'
    )

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def display_role_preset_match(
    players_data: List[Dict],
    df_filtered: pd.DataFrame,
    position_group: str,
    player_colors: List[str]
):
    """
    Display role/preset match ratings for selected players using circle rating system

    Shows how well each player matches different role/preset profiles using
    5-circle rating system (filled = good match, empty = poor match).
    Presets are sorted by score (highest first). Only shows roles relevant to
    each player's position.

    Args:
        players_data: List of selected player data dictionaries (with 'composite_attributes' and 'stats' keys)
        df_filtered: Filtered DataFrame with all players
        position_group: Position group (not used, preserved for compatibility)
        player_colors: List of colors for selected players
    """
    from config.defender_presets import DEFENDER_PRESETS
    from config.fullback_presets import FULLBACK_PRESETS
    from config.midfielder_presets import MIDFIELDER_PRESETS
    from config.forward_presets import FORWARD_PRESETS
    from config.attacking_midfielder_presets import ATTACKING_MIDFIELDER_PRESETS
    from utils.data_loader import get_player_stats
    from config.stat_categories import STAT_CATEGORIES
    from config.composite_attributes import COMPOSITE_ATTRIBUTES

    st.markdown("---")
    st.markdown("### Role Analysis")
    st.markdown(f"*Shows how well each player matches different tactical roles for {position_group}*")

    # Map individual positions to relevant preset categories
    position_preset_mapping = {
        # Defender positions
        'CB': DEFENDER_PRESETS,
        'Fullback': FULLBACK_PRESETS,
        'Defender': {**DEFENDER_PRESETS, **FULLBACK_PRESETS},
        'DM': MIDFIELDER_PRESETS,
        'AM': ATTACKING_MIDFIELDER_PRESETS,
        'Central Midfielder': {**DEFENDER_PRESETS, **ATTACKING_MIDFIELDER_PRESETS},
        
        'Winger': ATTACKING_MIDFIELDER_PRESETS,
        'Left Winger': ATTACKING_MIDFIELDER_PRESETS,
        'Right Winger': ATTACKING_MIDFIELDER_PRESETS,
        # Centre Forward positions
        'CF': FORWARD_PRESETS,
        'Forward': {**ATTACKING_MIDFIELDER_PRESETS, **FORWARD_PRESETS},
        'default': {**DEFENDER_PRESETS, **FORWARD_PRESETS, **ATTACKING_MIDFIELDER_PRESETS}
    }

    num_players = len(players_data)

    # Create columns for each player
    cols = st.columns(num_players)

    for idx, (col, player_data) in enumerate(zip(cols, players_data)):
        with col:
            player_name = player_data['info']['name']
            player_position = player_data['info']['position']

            st.markdown(f"#### {player_name}")
            st.caption(f"**Position:** {player_position}")

            # Get relevant presets based on this player's actual position
            relevant_presets = position_preset_mapping.get(
                position_group,
                position_preset_mapping['default']
            )

            # Calculate scores for all relevant presets
            preset_scores = []

            for preset_key, preset_config in relevant_presets.items():
                preset_icon = ''#preset_config.get('icon', '')
                preset_display = preset_config['display_name']

                # Calculate weighted score for this player
                components = preset_config.get('components', [])
                total_weight = 0
                weighted_sum = 0

                for component in components:
                    stat_name = component['stat']
                    weight = component['weight']

                    if stat_name in player_data['stats']:
                        stat_value = player_data['stats'][stat_name].get('percentile', 50.0)
                        weighted_sum += abs(weight) * stat_value
                        total_weight += abs(weight)

                # Normalize to 0-100 scale
                if total_weight > 0:
                    normalized_score = weighted_sum / total_weight
                else:
                    normalized_score = 50.0

                preset_scores.append({
                    'key': preset_key,
                    'icon': preset_icon,
                    'display': preset_display,
                    'score': normalized_score
                })

            # Sort by score descending (highest first)
            preset_scores.sort(key=lambda x: x['score'])

            # Create visualization
            fig, ax = plt.subplots(figsize=(9, len(preset_scores) * 0.7 + 1.5))
            fig.patch.set_facecolor('#f5f3e8')
            ax.set_facecolor('#f5f3e8')

            y_positions = range(len(preset_scores))
            preset_labels = [f"{ps['icon']} {ps['display']}" for ps in preset_scores]

            for y_pos, preset_score in enumerate(preset_scores):
                score = preset_score['score']
                color = player_colors[idx]

                

                # Draw 5 circles based on score
                circle_spacing = 1
                num_circles = 8
                last_circle_x = (num_circles - 1) * circle_spacing + 0.5
                score_x = last_circle_x + 0.6

                # Calculate number of filled circles (0-num_circles scale)
                circle_scale = 100/num_circles
                num_filled = int(score / circle_scale)
                partial_fill = (score % circle_scale) / circle_scale

                circle_size = 1600
                empty_color = '#bdc3c7'

                for circle_idx in range(num_circles):
                    x_pos = circle_idx * circle_spacing + 0.5
                    #x_pos = (num_circles - 1) * circle_spacing + 0.5

                    if circle_idx < num_filled:
                        fill_color = color
                        alpha = 1.0
                        edgecolor = 'white'
                        linewidth = 2
                    elif circle_idx == num_filled and partial_fill > 0:
                        fill_color = color
                        alpha = 0.4
                        edgecolor = 'white'
                        linewidth = 1
                    else:
                        fill_color = empty_color
                        alpha = 0.8
                        edgecolor = '#95a5a6'
                        linewidth = 0.5

                    ax.scatter(
                        x_pos,
                        y_pos,
                        s=circle_size,
                        c=fill_color,
                        alpha=alpha,
                        edgecolor=edgecolor,
                        linewidth=linewidth,
                        zorder=10
                    )

                # Add score label
                ax.text(
                    score_x,
                    y_pos,
                    f'{score:.0f}',
                    va='center',
                    ha='left',
                    fontsize=11,
                    fontweight='bold',
                    color='#2c3e50'
                )

            ax.set_yticks(y_positions)
            ax.set_yticklabels(preset_labels, fontsize=10, fontweight='bold')
            ax.set_xlabel('Role Rating', fontsize=10, fontweight='bold', color='#2c3e50')

            #ax.set_xlim(-0.5, 12.5)
            #ax.set_xlim(-0.2, 5 * circle_spacing + 2.5)
            ax.set_xlim(-0.3, score_x + 0.8)
            ax.set_ylim(-0.5, len(preset_scores) - 0.5)

            ax.grid(axis='y', alpha=0.2, linestyle='-', linewidth=0.5)
            ax.set_axisbelow(True)

            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#95a5a6')
            ax.spines['bottom'].set_color('#95a5a6')
            ax.set_xticks([])

            # Add legend for circles
            #legend_text = "●●●●● = Excellent Match | ●●●○○ = Good Match | ○○○○○ = Poor Match"
            legend_text = None
            ax.text(
                0,
                len(preset_scores) + 0.2,
                legend_text,
                fontsize=8,
                color='#7f8c8d',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', edgecolor='#95a5a6', linewidth=1)
            )

            plt.tight_layout()
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
