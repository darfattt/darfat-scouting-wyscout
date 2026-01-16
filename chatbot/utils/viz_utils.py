"""
Plotly visualization utilities
"""
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def create_radar_chart(players: List[Dict]) -> go.Figure:
    """
    Create radar/spider chart for player comparison
    
    Args:
        players: List of player dicts with composite_attrs
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    colors = ['#2ecc71', '#3498db', '#e67e22']
    
    if len(players) == 0:
        return fig
    
    composite_attrs = ['Security', 'ProgPass', 'BallCarrying', 'Creativity']
    
    for i, player in enumerate(players):
        values = []
        for attr in composite_attrs:
            comp_key = f'COMP_{attr}'
            if comp_key in player.get('composite_attrs', {}):
                values.append(player['composite_attrs'][comp_key].get('score', 50))
            else:
                values.append(50)
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=composite_attrs,
            fill='toself',
            name=player.get('name', 'Unknown'),
            line_color=colors[i % len(colors)],
            marker=dict(
                size=10,
                color=colors[i % len(colors)],
                opacity=0.7
            )
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='%'
            )
        ),
        showlegend=True,
        title="Player Attribute Profiles",
        height=500,
        paper_bgcolor='#f5f3e8'
    )
    
    return fig


def create_comparison_bar(players: List[Dict]) -> go.Figure:
    """
    Create horizontal bar chart for metric comparison
    
    Args:
        players: List of player dicts with stats
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    colors = ['#2ecc71', '#3498db']
    
    if len(players) == 0:
        return fig
    
    metrics = ['xG per 90', 'Goals per 90', 'Assists per 90']
    
    for i, player in enumerate(players):
        values = []
        labels = []
        
        stats = player.get('stats', {})
        for metric in metrics:
            if metric in stats:
                stat_data = stats[metric]
                values.append(stat_data.get('percentile', 50))
                value = stat_data.get('value', 0)
                labels.append(f"{metric} ({value:.2f})")
        
        if len(players) > 2:
            fig.add_trace(go.Bar(
                name=player.get('name', 'Unknown'),
                y=labels,
                x=values,
                orientation='h',
                marker_color=colors[i % len(colors)]
            ))
    
    fig.update_layout(
        title="Player Comparison (Percentiles)",
        xaxis_title="Percentile",
        yaxis_title="Metric",
        barmode='group' if len(players) > 2 else 'overlay',
        height=500,
        paper_bgcolor='#f5f3e8'
    )
    
    return fig


def create_scatter_plot(players: List[Dict], x_attr: str, y_attr: str) -> go.Figure:
    """
    Create scatter plot for player similarity
    
    Args:
        players: List of player dicts
        x_attr: Composite attribute for X-axis
        y_attr: Composite attribute for Y-axis
    
    Returns:
        Plotly Figure object
    """
    fig = go.Figure()
    
    x_values = []
    y_values = []
    names = []
    
    for player in players:
        comp_attrs = player.get('composite_attrs', {})
        
        x_key = f'COMP_{x_attr}'
        y_key = f'COMP_{y_attr}'
        
        x_values.append(comp_attrs.get(x_key, {}).get('score', 50))
        y_values.append(comp_attrs.get(y_key, {}).get('score', 50))
        names.append(player.get('name', 'Unknown'))
    
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='markers',
        text=names,
        textposition='top center',
        textfont=dict(size=9),
        marker=dict(
            size=12,
            color='#2ecc71',
            line=dict(width=1, color='#1a5276')
        ),
        hovertemplate='<b>%{text}</b><br>' +
                    f'{x_attr}: ' + '%{x:.1f}<br>' +
                    f'{y_attr}: ' + '%{y:.1f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=f"{x_attr} vs {y_attr}",
        xaxis_title=x_attr,
        yaxis_title=y_attr,
        height=600,
        paper_bgcolor='#f5f3e8'
    )
    
    return fig
