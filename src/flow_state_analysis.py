
# CogniStream - Day 9
# Developer Flow-State Scoring

from pathlib import Path
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent

SESSION_FILE = (
    ROOT / "data" / "processed"
    / "developer_sessions_cleaned.csv"
)

LOAD_FILE = (
    ROOT / "data" / "processed"
    / "cognitive_load_results.csv"
)

OUTPUT_FILE = (
    ROOT / "data" / "processed"
    / "flow_state_results.csv"
)

REPORT_FILE = ROOT / "reports" / "flow_state_report.txt"
CHART_DIR = ROOT / "reports" / "charts"


def analyze_flow_state():
    print("=" * 55)
    print("COGNISTREAM - FLOW-STATE ANALYSIS")
    print("=" * 55)

    if not SESSION_FILE.exists():
        raise FileNotFoundError(SESSION_FILE)

    if not LOAD_FILE.exists():
        raise FileNotFoundError(LOAD_FILE)

    sessions = pd.read_csv(SESSION_FILE)
    load_data = pd.read_csv(LOAD_FILE)

    required = [
        "session_id",
        "developer_id",
        "session_duration_min",
        "focused_time_min",
        "interruptions",
        "task_complexity",
    ]

    missing = [c for c in required if c not in sessions]
    if missing:
        raise ValueError(f"Missing session columns: {missing}")

    if not {
        "session_id",
        "cognitive_load_score"
    }.issubset(load_data.columns):
        raise ValueError("Cognitive load columns are missing")

    if sessions.empty or load_data.empty:
        raise ValueError("Input dataset is empty")

    if (
        sessions["session_id"].isna().any()
        or load_data["session_id"].isna().any()
        or not sessions["session_id"].is_unique
        or not load_data["session_id"].is_unique
    ):
        raise ValueError("Missing or duplicate session IDs")

    # Join Day 8 results with the cleaned sessions
    df = sessions.merge(
        load_data[["session_id", "cognitive_load_score"]],
        on="session_id",
        how="left",
        validate="one_to_one",
    )

    if df["cognitive_load_score"].isna().any():
        raise ValueError("Missing cognitive load results")

    if (df["session_duration_min"] <= 0).any():
        raise ValueError("Session duration must be positive")

    if not df["interruptions"].between(0, 10).all():
        raise ValueError("Interruptions outside expected range")

    if not df["task_complexity"].between(1, 5).all():
        raise ValueError("Invalid task complexity")

    if not df["cognitive_load_score"].between(0, 100).all():
        raise ValueError("Invalid cognitive load score")

    # 1. Focus efficiency, converted to 0-100
    df["focus_efficiency"] = (
        df["focused_time_min"]
        / df["session_duration_min"]
    ) * 100

    if not df["focus_efficiency"].between(0, 100).all():
        raise ValueError("Invalid focused time")

    # 2. Interruptions: fewer means a higher score
    df["interruption_score"] = (
        100 - df["interruptions"] * 10
    )

    # 3. Workload balance:
    # In this illustrative model, moderate load
    # (score 50) is treated as most favorable.
    df["load_balance_score"] = (
        100 - 2 * (
            df["cognitive_load_score"] - 50
        ).abs()
    ).clip(lower=0, upper=100)

    # 4. Flow score (heuristic, not validated)
    df["flow_state_score"] = (
        0.60 * df["focus_efficiency"]
        + 0.25 * df["interruption_score"]
        + 0.15 * df["load_balance_score"]
    ).round(2)

    def classify_flow(score):
        if score < 40:
            return "Low Flow"
        elif score < 70:
            return "Moderate Flow"
        return "High Flow"

    df["flow_state_level"] = (
        df["flow_state_score"].apply(classify_flow)
    )

    # Sort records for consistent output
    df = df.sort_values(
        "session_id"
    ).reset_index(drop=True)

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

    # Summary statistics
    avg_flow = df["flow_state_score"].mean()

    flow_counts = (
        df["flow_state_level"]
        .value_counts()
        .reindex(
            ["Low Flow", "Moderate Flow", "High Flow"],
            fill_value=0
        )
    )

    developer_flow = (
        df.groupby("developer_id")["flow_state_score"]
        .mean()
        .sort_index()
    )

    print(f"\nTotal sessions: {len(df)}")
    print(f"Developers: {df['developer_id'].nunique()}")
    print(f"Average flow-state score: {avg_flow:.2f}")

    print("\nFLOW-STATE DISTRIBUTION")
    print(flow_counts.to_string())

    print("\nAVERAGE FLOW SCORE BY DEVELOPER")
    print(developer_flow.round(2).to_string())

    # Chart 1: Flow-state distribution
    plt.figure(figsize=(8, 5))
    plt.bar(flow_counts.index, flow_counts.values)
    plt.title("Estimated Flow-State Distribution")
    plt.xlabel("Flow-State Category")
    plt.ylabel("Number of Sessions")
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "flow_state_distribution.png",
        dpi=150
    )
    plt.close()

    # Chart 2: Average flow score by developer
    plt.figure(figsize=(10, 5))
    plt.bar(
        developer_flow.index,
        developer_flow.values
    )
    plt.title("Average Estimated Flow Score by Developer")
    plt.xlabel("Anonymous Developer ID")
    plt.ylabel("Average Flow Score (0-100)")
    plt.ylim(0, 100)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        CHART_DIR / "developer_flow_scores.png",
        dpi=150
    )
    plt.close()

    report = [
        "COGNISTREAM - FLOW-STATE ANALYSIS REPORT",
        "=" * 50,
        "Source: Synthetic developer work sessions",
        f"Total sessions: {len(df)}",
        f"Unique developers: {df['developer_id'].nunique()}",
        f"Average estimated flow score: {avg_flow:.2f}",
        "",
        "FLOW-STATE DISTRIBUTION",
        flow_counts.to_string(),
        "",
        "AVERAGE FLOW SCORE BY DEVELOPER",
        developer_flow.round(2).to_string(),
        "",
        "SCORING METHODOLOGY",
        "60% focus efficiency",
        "25% interruption score",
        "15% estimated cognitive load balance",
        "",
        "Low Flow: below 40",
        "Moderate Flow: 40 to below 70",
        "High Flow: 70 and above",
        "",
        "LIMITATIONS",
        "This is a heuristic demonstration metric.",
        "Weights and categories have not been validated.",
        "All input records are synthetic.",
        "It does not confirm psychological flow.",
        "Not suitable for real employee assessment."
    ]

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print("\nFlow-state analysis completed successfully!")
    print(f"CSV saved: {OUTPUT_FILE}")
    print(f"Report saved: {REPORT_FILE}")
    print("Charts generated: 2")


if __name__ == "__main__":
    analyze_flow_state()

