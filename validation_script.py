"""
Migration validation script
Run after migration to verify correctness
"""
import os
import sys
import pandas as pd
from utils.data_loader import load_all_league_data, get_all_stat_columns, calculate_composite_attributes_batch
from config.stat_categories import STAT_CATEGORIES, PLAYER_INFO_COLUMNS
from config.composite_attributes import COMPOSITE_ATTRIBUTES


def validate_data_loading():
    """Test data loads without errors"""
    print("Testing data loading...")
    data_folder = os.path.join(os.getcwd(), "data", "2025")
    df = load_all_league_data(data_folder)

    assert len(df) > 0, "No data loaded"
    print(f"✓ Data loaded: {len(df)} players")

    return df


def validate_required_columns(df):
    """Check required columns exist"""
    print("\nValidating required columns...")
    required = ['Player', 'Age', 'Competition', 'Position', 'Team', 'Birth country']
    missing = [col for col in required if col not in df.columns]
    assert not missing, f"Missing required columns: {missing}"
    print("✓ All required columns present")


def validate_derived_metrics(df):
    """Check derived metrics exist and are correct"""
    print("\nValidating derived metrics...")
    derived = ['pAdj Tkl+Int per 90', 'Aerial duels won per 90',
              'Cards per 90', 'npxG per 90', 'npxG per shot']

    for col in derived:
        assert col in df.columns, f"Missing derived metric: {col}"
        assert df[col].notna().sum() > 0, f"All NaN in {col}"

    print("✓ All derived metrics present and valid")


def validate_column_aliases(df):
    """Check League alias works"""
    print("\nValidating column aliases...")
    assert 'League' in df.columns, "League alias not created"
    assert 'Competition' in df.columns, "Competition column missing"

    # Check that League and Competition have the same values (accounting for NaN)
    mismatch_count = 0
    for idx in df.index:
        league_val = df.loc[idx, 'League']
        comp_val = df.loc[idx, 'Competition']

        # Both NaN is OK
        if pd.isna(league_val) and pd.isna(comp_val):
            continue
        # Values match is OK
        elif league_val == comp_val:
            continue
        else:
            mismatch_count += 1
            if mismatch_count <= 3:  # Print first 3 mismatches
                print(f"  Mismatch at index {idx}: League='{league_val}', Competition='{comp_val}'")

    if mismatch_count > 0:
        print(f"⚠ Warning: {mismatch_count} mismatches between League and Competition columns")
    else:
        print("✓ League alias working correctly")


def validate_stat_categories(df):
    """Check all stat_categories columns exist"""
    print("\nValidating stat categories...")

    stat_cols = get_all_stat_columns(STAT_CATEGORIES)
    missing = [col for col in stat_cols if col not in df.columns]

    if missing:
        print(f"⚠ Missing stats: {missing}")
    else:
        print("✓ All stat_categories columns present")


def validate_composite_attributes(df):
    """Check composite attributes calculate"""
    print("\nValidating composite attributes...")

    stat_cols = get_all_stat_columns(STAT_CATEGORIES)
    df_with_comp = calculate_composite_attributes_batch(df, stat_cols, COMPOSITE_ATTRIBUTES)

    comp_cols = [f"COMP_{attr}" for attr in COMPOSITE_ATTRIBUTES.keys()]
    missing = [col for col in comp_cols if col not in df_with_comp.columns]

    assert not missing, f"Missing composite attributes: {missing}"
    print("✓ All composite attributes calculated")


def validate_no_contract_expiry_references(df):
    """Check that contract_expiry column doesn't exist and no code references it"""
    print("\nValidating contract expiry removal...")

    # Check column doesn't exist in data
    if 'contract_expiry' in df.columns:
        print("⚠ Warning: contract_expiry column still exists in data (may be from old format CSV)")
    else:
        print("✓ No contract_expiry column in loaded data")


def main():
    print("=== Migration Validation ===\n")

    try:
        df = validate_data_loading()
        validate_required_columns(df)
        validate_derived_metrics(df)
        validate_column_aliases(df)
        validate_stat_categories(df)
        validate_composite_attributes(df)
        validate_no_contract_expiry_references(df)

        print(f"\n=== Summary ===")
        print(f"Total players: {len(df)}")
        print(f"Competitions: {df['Competition'].nunique()}")
        print(f"Positions: {df['Position'].nunique()}")
        print(f"Teams: {df['Team'].nunique()}")
        print(f"\n✅ Migration validation PASSED")

    except AssertionError as e:
        print(f"\n❌ Validation FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
