
# CogniStream - Day 6
# Exploratory Data Analysis

from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "processed" / "developer_sessions_cleaned.csv"
REPORT_DIR = ROOT / "reports"
CHART_DIR = REPORT_DIR / "charts"

REPORT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


def run_analysis():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Cleaned dataset missing: {DATA_FILE}"
        )

    df = pd.read_csv(DATA_FILE, parse_dates=["date"])

    print("=" * 55)
    print("COGNISTREAM - EXPLORATORY DATA ANALYSIS")
    print("=" * 55)

    print(f"Total sessions: {len(df)}")
    print(f"Unique developers: {df['developer_id'].nunique()}")

    # Summary statistics
    mean_focus = df["focused_time_min"].mean()
    mean_productivity = df["productivity_score"].mean()
    mean_interruptions = df["interruptions"].mean()

    # Focus ratio measures portion of session spent focused
    df["focus_ratio"] = (
        df["focused_time_min"]
        / df["session_duration_min"]
    )

    mean_focus_ratio = df["focus_ratio"].mean()

    print(f"Average focused time: {mean_focus:.2f} minutes")
    print(f"Average productivity: {mean_productivity:.2f}")
    print(f"Average interruptions: {mean_interruptions:.2f}")
    print(f"Average focus ratio: {mean_focus_ratio:.2%}")

    # Chart 1: Task type distribution
    task_counts = df["task_type"].value_counts()

    plt.figure(figsize=(9, 5))
    task_counts.plot(kind="bar")
    plt.title("Developer Work Sessions by Task Type")
    plt.xlabel("Task Type")
    plt.ylabel("Number of Sessions")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "task_distribution.png", dpi=150)
    plt.close()

    # Chart 2: Focus time distribution
    plt.figure(figsize=(9, 5))
    plt.hist(df["focused_time_min"], bins=20)
    plt.title("Distribution of Developer Focus Time")
    plt.xlabel("Focused Time (Minutes)")
    plt.ylabel("Number of Sessions")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "focus_distribution.png", dpi=150)
    plt.close()

    # Chart 3: Interruptions vs productivity
    summary = (
        df.groupby("interruptions")["productivity_score"]
        .mean()
        .sort_index()
    )

    plt.figure(figsize=(9, 5))
    plt.plot(summary.index, summary.values, marker="o")
    plt.title("Interruptions vs Average Productivity")
    plt.xlabel("Number of Interruptions")
    plt.ylabel("Average Productivity Score")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "interruptions_productivity.png",
        dpi=150
    )
    plt.close()

    # Chart 4: Task complexity vs focus ratio
    complexity = (
        df.groupby("task_complexity")["focus_ratio"]
        .mean()
        .sort_index()
    )

    plt.figure(figsize=(9, 5))
    plt.bar(complexity.index, complexity.values)
    plt.title("Average Focus Ratio by Task Complexity")
    plt.xlabel("Task Complexity (1-5)")
    plt.ylabel("Average Focus Ratio")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "complexity_focus.png", dpi=150)
    plt.close()

    # Save analysis report
    report = [
        "COGNISTREAM - EDA REPORT",
        "=" * 45,
        "Source: Synthetic developer sessions",
        f"Total sessions: {len(df)}",
        f"Unique developers: {df['developer_id'].nunique()}",
        f"Average focus time: {mean_focus:.2f} minutes",
        f"Average productivity score: {mean_productivity:.2f}",
        f"Average interruptions: {mean_interruptions:.2f}",
        f"Average focus ratio: {mean_focus_ratio:.2%}",
        "",
        "TASK TYPE DISTRIBUTION",
        task_counts.to_string(),
        "",
        "AVERAGE PRODUCTIVITY BY INTERRUPTION COUNT",
        summary.to_string(),
        "",
        "AVERAGE FOCUS RATIO BY TASK COMPLEXITY",
        complexity.to_string(),
        "",
        "NOTE: Productivity and workload indicators are",
        "simulated metrics, not real employee measurements.",
        "Relationships in this generated dataset should",
        "not be interpreted as causal evidence."
    ]

    report_file = REPORT_DIR / "eda_report.txt"
    report_file.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nEDA completed successfully!")
    print(f"Report saved: {report_file}")
    print(f"Charts saved: {CHART_DIR}")
    print("Total charts generated: 4")


if __name__ == "__main__":
    run_analysis()
