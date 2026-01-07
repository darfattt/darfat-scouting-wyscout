# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Streamlit-based football player comparison application for analyzing players from various leagues using Wyscout data. The app allows side-by-side comparison of 2-3 players across defensive, progressive, and offensive statistics, with support for multiple positions (currently CB and DM/CM).

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## Architecture

### Core Application Flow

1. **app.py**: Main Streamlit application entry point
   - Handles UI layout and player selection
   - Manages position type selection (CB vs DM/CM)
   - Caches data loading using `@st.cache_data`
   - Loads position-specific CSV files from root directory

2. **Data Processing Pipeline**:
   - Load CSV → Filter by position → Calculate percentiles → Display comparisons
   - All statistics are converted to percentile ranks (0-100) for standardized comparison
   - CSV files are pre-filtered by position (no runtime position filtering needed)

3. **Configuration System**:
   - **config/stat_categories.py**: Defines which stats appear in each category (Defensive, Progressive, Offensive, General)
   - **config/composite_attributes.py**: Weighted formulas for calculating composite attributes (Flair, Tackling, Passing, Positioning, Composure, Anticipation)
   - **config/position_rankings.py**: Maps which composite attributes are most relevant for each position type

4. **Utility Modules**:
   - **utils/data_loader.py**: CSV loading, percentile calculations, composite attribute computation
   - **utils/visualizations.py**: Matplotlib chart generation and Streamlit display functions

### Data Structure

- **Player CSV Files**: Located in root directory (e.g., `elliteserrien_cb_2025-10-15T04-08_export.csv`)
- **Additional Data**: `data/2025/` contains various league exports from Wyscout
- **Required Columns**: Player, Age, Team, Birth country, Position, plus all stat columns defined in STAT_CATEGORIES

### Key Design Patterns

- **Percentile-based Comparisons**: All raw statistics are converted to percentiles within the filtered dataset for fair comparison
- **Composite Attributes**: Weighted combinations of multiple stats (e.g., Tackling = 30% Defensive duels won + 25% pAdj Tkl+Int + 25% Defensive actions - 10% Fouls)
- **Position-specific Analysis**: Different composite attributes are highlighted based on position type (DM/CM emphasizes Flair/Tackling, CB emphasizes Positioning/Anticipation)
- **Side-by-side Visualization**: Each player gets their own column with complete stat breakdown

## Adding New Features

### Adding a New Position Type

1. Add position CSV file to root directory
2. Update `csv_files` dictionary in `app.py:load_data()`
3. Add position to radio selection in `app.py:main()`
4. Add position label to `position_labels` dictionary
5. Define key attributes in `config/position_rankings.py`

### Adding New Statistics

1. Add stat definition to appropriate category in `config/stat_categories.py`
2. Ensure CSV file contains the column name specified
3. Stats are automatically included in percentile calculations

### Adding New Composite Attributes

1. Define attribute in `config/composite_attributes.py` with:
   - `display_name`: Human-readable name
   - `description`: What the attribute measures
   - `components`: List of stats with weights (negative weights for inverse stats)
   - `icon`: Emoji for visual display
2. Add to position's `key_attributes` in `config/position_rankings.py` if relevant

## Important Implementation Details

- **UTF-8 BOM Encoding**: CSV files use `utf-8-sig` encoding to handle BOM (see `data_loader.py:20`)
- **Unnamed Column Handling**: First unnamed column is automatically removed from CSV (see `data_loader.py:23-24`)
- **Color Scheme**: Player colors are fixed as Green (#2ecc71), Blue (#3498db), Orange (#e67e22)
- **Background Color**: Consistent `#f5f3e8` cream background across all visualizations
- **Cache Management**: Data loading is cached by position type to improve performance

## Data File Conventions

- CSV exports from Wyscout follow naming pattern: `{league}_{position}_{timestamp}_export.csv`
- Position-specific files are pre-filtered and should contain only relevant positions
- All statistics must be numeric; percentages are stored as numbers (e.g., 75.5 not "75.5%")
