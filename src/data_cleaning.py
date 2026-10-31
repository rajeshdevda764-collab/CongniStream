
# CogniStream - Day 5
# Data Cleaning and Preprocessing

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "developer_sessions.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "developer_sessions_cleaned.csv"
REPORT_FILE = ROOT / "reports" / "data_cleaning_report.txt"

NUMERIC_COLUMNS = [
    "session_duration_min",
    "focused_time_min",
    "interruptions",
    "task_complexity",
    "perceived_workload",
    "completed_tasks",
    "productivity_score",
]


def clean_data():
    if not INPUT_FILE.exists():
        print(f"ERROR: File not found: {INPUT_FILE}")
        return

    print("=" * 55)
    print("COGNISTREAM - DATA CLEANING")
    print("=" * 55)

    df = pd.read_csv(INPUT_FILE)
    original_rows = len(df)

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    required_columns = [
        "session_id", "developer_id", "date", "task_type",
        *NUMERIC_COLUMNS
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Remove exact duplicate records
    duplicate_rows = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Normalize text columns
    for col in ["session_id", "developer_id", "task_type"]:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)

    # Convert numeric data types
    for col in NUMERIC_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remove records with invalid essential values
    essential_columns = [
        "session_id", "developer_id", "date", "task_type",
        *NUMERIC_COLUMNS
    ]

    invalid_or_missing = df[essential_columns].isna().any(axis=1)

    # Enforce numeric ranges
    valid_ranges = (
        df["session_duration_min"].between(1, 1440)
        & df["focused_time_min"].ge(0)
        & (
            df["focused_time_min"]
            <= df["session_duration_min"]
        )
        & df["interruptions"].ge(0)
        & df["task_complexity"].between(1, 5)
        & df["perceived_workload"].between(1, 5)
        & df["completed_tasks"].ge(0)
        & df["productivity_score"].between(0, 100)
    )

    # Validate whole-number fields
    integer_columns = [
        "session_duration_min",
        "focused_time_min",
        "interruptions",
        "task_complexity",
        "perceived_workload",
        "completed_tasks"
    ]

    for col in integer_columns:
        valid_ranges &= df[col].mod(1).eq(0)

    valid_mask = ~invalid_or_missing & valid_ranges
    invalid_records = int((~valid_mask).sum())

    df = df.loc[valid_mask].copy()

    # Retain first occurrence of each session ID
    duplicate_ids = int(df["session_id"].duplicated().sum())
    df = df.drop_duplicates(
        subset=["session_id"], keep="first"
    ).copy()

    # Sort by date and session ID
    df = df.sort_values(
        ["date", "session_id"]
    ).reset_index(drop=True)

    # Standardize dates for CSV
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Validate the cleaned dataset
    assert not df.empty, "Cleaned dataset is empty!"
    assert df["session_id"].is_unique
    assert df.isna().sum().sum() == 0

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    removed_rows = original_rows - len(df)

    report = (
        "COGNISTREAM - DATA CLEANING REPORT\n"
        + "=" * 45 + "\n"
        + f"Original records: {original_rows}\n"
        + f"Exact duplicate rows: {duplicate_rows}\n"
        + f"Invalid or missing records removed: {invalid_records}\n"
        + f"Duplicate session IDs removed: {duplicate_ids}\n"
        + f"Total records removed: {removed_rows}\n"
        + f"Cleaned records: {len(df)}\n"
        + f"Columns: {len(df.columns)}\n"
        + f"Remaining missing values: {df.isna().sum().sum()}\n"
        + f"Remaining duplicate IDs: "
        + f"{df['session_id'].duplicated().sum()}\n"
        + "\nData source: Synthetic developer session data.\n"
    )

    REPORT_FILE.write_text(report, encoding="utf-8")

    print(report)
    print(f"Cleaned CSV: {OUTPUT_FILE}")
    print(f"Cleaning report: {REPORT_FILE}")


if __name__ == "__main__":
    clean_data()
