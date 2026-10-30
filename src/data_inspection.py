
# CogniStream - Day 4
# Developer Work-Session Data Inspection

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = PROJECT_ROOT / "data" / "developer_sessions.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "data_inspection.txt"


def inspect_dataset():
    print("=" * 55)
    print("COGNISTREAM - DATA INSPECTION")
    print("=" * 55)

    if not DATA_FILE.exists():
        print("ERROR: Dataset not found!")
        print(f"Expected location: {DATA_FILE}")
        return

    df = pd.read_csv(DATA_FILE)

    print("\n1. DATASET OVERVIEW")
    print(f"Total rows: {len(df)}")
    print(f"Total columns: {len(df.columns)}")

    print("\n2. FIRST FIVE RECORDS")
    print(df.head().to_string(index=False))

    print("\n3. COLUMN NAMES AND DATA TYPES")
    print(df.dtypes.to_string())

    print("\n4. MISSING VALUES")
    missing = df.isnull().sum()
    print(missing.to_string())

    print("\n5. DUPLICATE RECORDS")
    duplicates = df.duplicated().sum()
    duplicate_ids = df["session_id"].duplicated().sum()
    print(f"Duplicate rows: {duplicates}")
    print(f"Duplicate session IDs: {duplicate_ids}")

    print("\n6. NUMERICAL STATISTICS")
    stats = df.describe()
    print(stats.to_string())

    print("\n7. SESSION SUMMARY")
    print(f"Unique developers: {df['developer_id'].nunique()}")
    print(f"Unique task types: {df['task_type'].nunique()}")
    print(
        "Average session duration: "
        f"{df['session_duration_min'].mean():.2f} minutes"
    )
    print(
        "Average focused time: "
        f"{df['focused_time_min'].mean():.2f} minutes"
    )
    print(
        "Average productivity score: "
        f"{df['productivity_score'].mean():.2f}"
    )

    print("\n8. TASK TYPE DISTRIBUTION")
    print(df["task_type"].value_counts().to_string())

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open("w", encoding="utf-8") as report:
        report.write("COGNISTREAM - DATA INSPECTION REPORT\n")
        report.write("=" * 45 + "\n\n")
        report.write(f"Total records: {len(df)}\n")
        report.write(f"Total columns: {len(df.columns)}\n")
        report.write(
            f"Missing values: {df.isnull().sum().sum()}\n"
        )
        report.write(f"Duplicate rows: {duplicates}\n")
        report.write(f"Duplicate session IDs: {duplicate_ids}\n")
        report.write(
            f"Unique developers: {df['developer_id'].nunique()}\n"
        )
        report.write("\nColumn data types:\n")
        report.write(df.dtypes.to_string())
        report.write("\n\nNumerical statistics:\n")
        report.write(stats.to_string())
        report.write("\n\nTask type distribution:\n")
        report.write(df["task_type"].value_counts().to_string())

    print("\nInspection report generated successfully!")
    print(f"Saved to: {REPORT_FILE}")


if __name__ == "__main__":
    inspect_dataset()
