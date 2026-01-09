import os
import pandas as pd
from pathlib import Path


def load_expiry_data(expiry_dir: str) -> set:
    """
    Load all expiry CSV files and create a set of (player, team) tuples

    Args:
        expiry_dir: Path to directory containing expiry CSV files

    Returns:
        Set of lowercase (player, team) tuples
    """
    expiry_set = set()
    expiry_path = Path(expiry_dir)

    for csv_file in expiry_path.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file, encoding="utf-8-sig")
            if "Player" in df.columns and "Team" in df.columns:
                for _, row in df.iterrows():
                    player = str(row["Player"]).lower() if pd.notna(row["Player"]) else ""
                    team = str(row["Team"]).lower() if pd.notna(row["Team"]) else ""
                    if player and team:
                        expiry_set.add((player, team))
        except Exception:
            pass

    return expiry_set


def process_csv_file(source_path: Path, output_path: Path, expiry_set: set) -> None:
    """
    Process a single CSV file and add contract_expiry column

    Args:
        source_path: Path to source CSV file
        output_path: Path to save processed CSV file
        expiry_set: Set of (player, team) tuples that are expiring
    """
    try:
        df = pd.read_csv(source_path, encoding="utf-8-sig")

        if "Player" in df.columns and "Team" in df.columns:
            df["contract_expiry"] = False

            for idx, row in df.iterrows():
                player = str(row["Player"]).lower() if pd.notna(row["Player"]) else ""
                team = str(row["Team"]).lower() if pd.notna(row["Team"]) else ""
                if (player, team) in expiry_set:
                    df.at[idx, "contract_expiry"] = True

        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False, encoding="utf-8-sig")

    except Exception:
        pass


def main():
    """
    Main function to process all CSV files and add contract expiry information
    """
    source_base = Path("data/pre/2025")
    output_base = Path("data/post/2025")
    expiry_dir = Path("data/pre/expiry")

    expiry_set = load_expiry_data(expiry_dir)

    for csv_file in source_base.rglob("*.csv"):
        relative_path = csv_file.relative_to(source_base)
        output_path = output_base / relative_path
        process_csv_file(csv_file, output_path, expiry_set)


if __name__ == "__main__":
    main()
