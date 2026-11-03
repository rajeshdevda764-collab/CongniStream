
# CogniStream - Day 8
# Cognitive Load Analytics

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

OUTPUT_FILE = (
    ROOT / "data" / "processed"
    / "cognitive_load_results.csv"
)

REPORT_FILE = (
    ROOT / "reports" / "cognitive_load_report.txt"
)

CHART_DIR = ROOT / "reports" / "charts"


def analyze_cognitive_load():

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE}"
        )

    print("=" * 55)
    print("COGNISTREAM - COGNITIVE LOAD ANALYSIS")
    print("=" * 55)

    df = pd.read_csv(DATA_FILE)

    required = [
        "session_id",
        "developer_id",
        "task_complexity",
        "interruptions",
        "perceived_workload",
        "session_duration_min",
        "focused_time_min",
    ]

    missing = [
        col for col in required if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    if df.empty:
        raise ValueError("Dataset is empty")

    if (df["session_duration_min"] <= 0).any():
        raise ValueError("Invalid session duration")

    if not df["task_complexity"].between(1, 5).all():
        raise ValueError("Invalid task complexity")

    if not df["perceived_workload"].between(1, 5).all():
        raise ValueError("Invalid workload values")

    if not df["interruptions"].between(0, 10).all():
        raise ValueError("Interruptions outside expected range")

    # Calculate focus ratio
    df["focus_ratio"] = (
        df["focused_time_min"]
        / df["session_duration_min"]
    )

    if not df["focus_ratio"].between(0, 1).all():
        raise ValueError("Invalid focus ratio")

    # Normalize all indicators to a 0-100 scale
    complexity_score = (
        (df["task_complexity"] - 1) / 4
    ) * 100

    interruption_score = (
        df["interruptions"] / 10
    ) * 100

    workload_score = (
        (df["perceived_workload"] - 1) / 4
    ) * 100

    # Heuristic cognitive load estimate
    # Weights are design assumptions, not validated.
    df["cognitive_load_score"] = (
        0.40 * complexity_score
        + 0.30 * interruption_score
        + 0.30 * workload_score
    ).round(2)

    # Categorize estimated cognitive load
    def classify_load(score):
        if score < 35:
            return "Low"
        elif score < 70:
            return "Moderate"
        return "High"

    df["cognitive_load_level"] = (
        df["cognitive_load_score"].apply(classify_load)
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True, exist_ok=True
    )

    REPORT_FILE.parent.mkdir(
        parents=True, exist_ok=True
    )

    CHART_DIR.mkdir(
        parents=True, exist_ok=True
    )

    df.to_csv(OUTPUT_FILE, index=False)

    # Overall metrics
    average_load = df["cognitive_load_score"].mean()

    load_counts = (
        df["cognitive_load_level"]
        .value_counts()
        .reindex(
            ["Low", "Moderate", "High"],
            fill_value=0
        )
    )

    # Developer-level comparison
    developer_load = (
        df.groupby("developer_id")["cognitive_load_score"]
        .mean()
        .sort_index()
    )

    print(f"\nTotal sessions: {len(df)}")
    print(f"Developers: {df['developer_id'].nunique()}")
    print(f"Average cognitive load: {average_load:.2f}")

    print("\nCOGNITIVE LOAD DISTRIBUTION")
    print(load_counts.to_string())

    print("\nAVERAGE COGNITIVE LOAD BY DEVELOPER")
    print(developer_load.round(2).to_string())

    # Chart 1: Cognitive load distribution
    plt.figure(figsize=(8, 5))

    plt.bar(
        load_counts.index,
        load_counts.values
    )

    plt.title("Estimated Cognitive Load Distribution")
    plt.xlabel("Cognitive Load Level")
    plt.ylabel("Number of Sessions")
    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "cognitive_load_distribution.png",
        dpi=150
    )
    plt.close()

    # Chart 2: Cognitive load by developer
    plt.figure(figsize=(10, 5))

    plt.bar(
        developer_load.index,
        developer_load.values
    )

    plt.title("Average Estimated Cognitive Load by Developer")
    plt.xlabel("Anonymous Developer ID")
    plt.ylabel("Average Cognitive Load Score")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "developer_cognitive_load.png",
        dpi=150
    )
    plt.close()

    # Save the report
    report = [
        "COGNISTREAM - COGNITIVE LOAD REPORT",
        "=" * 50,
        "Source: Synthetic developer session dataset",
        f"Total sessions: {len(df)}",
        f"Average estimated load: {average_load:.2f}",
        "",
        "COGNITIVE LOAD LEVELS",
        load_counts.to_string(),
        "",
        "AVERAGE LOAD BY DEVELOPER",
        developer_load.round(2).to_string(),
        "",
        "SCORING METHODOLOGY",
        "40% task complexity",
        "30% interruptions",
        "30% simulated workload",
        "",
        "Low: score below 35",
        "Moderate: score from 35 to below 70",
        "High: score 70 or above",
        "",
        "LIMITATIONS",
        "This is a heuristic score for demonstration.",
        "The weights and thresholds are not validated.",
        "The workload data is simulated.",
        "It is not a clinical or psychological assessment.",
        "Scores should not be used to evaluate employees."
    ]

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nCognitive load analysis completed successfully!")
    print(f"CSV saved: {OUTPUT_FILE}")
    print(f"Report saved: {REPORT_FILE}")
    print("Charts generated: 2")


if __name__ == "__main__":
    analyze_cognitive_load()
