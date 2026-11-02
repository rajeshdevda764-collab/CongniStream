
# CogniStream - Day 7
# Developer Productivity Analysis

from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = (
    ROOT / "data" / "processed"
    / "developer_sessions_cleaned.csv"
)

REPORT_DIR = ROOT / "reports"
CHART_DIR = REPORT_DIR / "charts"
OUTPUT_FILE = (
    ROOT / "data" / "processed"
    / "developer_productivity_summary.csv"
)

def analyze_productivity():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(DATA_FILE)

    required = [
        "developer_id",
        "session_duration_min",
        "focused_time_min",
        "interruptions",
        "completed_tasks",
        "productivity_score",
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df.empty:
        raise ValueError("Dataset is empty")

    if (df["session_duration_min"] <= 0).any():
        raise ValueError("Invalid session duration found")

    print("=" * 55)
    print("COGNISTREAM - DEVELOPER PRODUCTIVITY ANALYSIS")
    print("=" * 55)

    # Session-level focus efficiency
    df["focus_efficiency"] = (
        df["focused_time_min"]
        / df["session_duration_min"]
    ) * 100

    # Per-developer summary
    summary = df.groupby("developer_id").agg(
        total_sessions=("session_id", "count"),
        total_work_min=("session_duration_min", "sum"),
        total_focus_min=("focused_time_min", "sum"),
        average_interruptions=("interruptions", "mean"),
        completed_tasks=("completed_tasks", "sum"),
        average_productivity=("productivity_score", "mean")
    ).reset_index()

    # Weighted focus efficiency
    summary["focus_efficiency"] = (
        summary["total_focus_min"]
        / summary["total_work_min"] * 100
    )

    # Tasks per focused hour
    summary["tasks_per_focus_hour"] = (
        summary["completed_tasks"]
        / (summary["total_focus_min"] / 60)
    )

    summary = summary.sort_values(
        "developer_id"
    ).reset_index(drop=True)

    numeric_cols = [
        "average_interruptions",
        "average_productivity",
        "focus_efficiency",
        "tasks_per_focus_hour",
    ]

    summary[numeric_cols] = (
        summary[numeric_cols].round(2)
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True, exist_ok=True
    )
    summary.to_csv(OUTPUT_FILE, index=False)

    print("\n1. DATASET OVERVIEW")
    print(f"Total sessions: {len(df)}")
    print(
        f"Developers analyzed: "
        f"{summary['developer_id'].nunique()}"
    )

    print("\n2. DEVELOPER PRODUCTIVITY SUMMARY")
    print(summary.to_string(index=False))

    print("\n3. OVERALL METRICS")
    overall_focus = (
        df["focused_time_min"].sum()
        / df["session_duration_min"].sum() * 100
    )
    print(f"Overall focus efficiency: {overall_focus:.2f}%")
    print(
        "Average simulated productivity: "
        f"{df['productivity_score'].mean():.2f}"
    )
    print(
        "Total simulated completed tasks: "
        f"{df['completed_tasks'].sum()}"
    )

    # Chart 1: Mean productivity by developer
    plt.figure(figsize=(10, 5))
    plt.bar(
        summary["developer_id"],
        summary["average_productivity"]
    )
    plt.title("Average Productivity Score by Developer")
    plt.xlabel("Anonymous Developer ID")
    plt.ylabel("Mean Simulated Productivity (0-100)")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "developer_productivity.png",
        dpi=150
    )
    plt.close()

    # Chart 2: Focus efficiency by developer
    plt.figure(figsize=(10, 5))
    plt.bar(
        summary["developer_id"],
        summary["focus_efficiency"]
    )
    plt.title("Focus Efficiency by Developer")
    plt.xlabel("Anonymous Developer ID")
    plt.ylabel("Focused Time / Session Time (%)")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "developer_focus_efficiency.png",
        dpi=150
    )
    plt.close()

    report_lines = [
        "COGNISTREAM - DEVELOPER PRODUCTIVITY REPORT",
        "=" * 50,
        "Dataset: Synthetic developer work sessions",
        f"Total sessions: {len(df)}",
        f"Developers: {summary['developer_id'].nunique()}",
        f"Overall focus efficiency: {overall_focus:.2f}%",
        "",
        "PER-DEVELOPER SUMMARY",
        summary.to_string(index=False),
        "",
        "METRIC DEFINITIONS",
        "Focus efficiency = total focused minutes / total work minutes * 100",
        "Tasks per focus hour = completed tasks / focused hours",
        "Average productivity = mean synthetic productivity score",
        "",
        "IMPORTANT NOTE",
        "This analysis uses simulated data.",
        "Results are not real employee performance assessments.",
        "Productivity scores depend on the dataset generator's assumptions."
    ]

    report_file = (
        REPORT_DIR / "developer_productivity_report.txt"
    )

    report_file.write_text(
        "\n".join(report_lines),
        encoding="utf-8"
    )

    print("\nProductivity analysis completed successfully!")
    print(f"Summary CSV: {OUTPUT_FILE}")
    print(f"Report: {report_file}")
    print("Charts generated: 2")


if __name__ == "__main__":
    analyze_productivity()
