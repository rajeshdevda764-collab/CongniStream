import os
import numpy as np
import pandas as pd

# Reproducible sample data
np.random.seed(42)

# Project folders
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("results", exist_ok=True)
os.makedirs("charts", exist_ok=True)

# Generate sample developer activity
n = 1000

data = pd.DataFrame({
    "developer_id": np.random.randint(1, 31, n),
    "date": pd.date_range("2026-09-01", periods=n, freq="h"),
    "session_duration_min": np.random.randint(20, 241, n),
    "focus_score": np.random.randint(30, 101, n),
    "interruptions": np.random.poisson(3, n),
    "tasks_completed": np.random.poisson(2, n),
    "meetings_count": np.random.poisson(1, n),
})

# Create an illustrative cognitive-load proxy (0-100)
load = (
    100
    - 0.35 * data["focus_score"]
    + 3 * data["interruptions"]
    + 2 * data["meetings_count"]
    - 2 * data["tasks_completed"]
    + np.random.normal(0, 8, n)
)

data["cognitive_load_score"] = np.clip(load, 0, 100).round(2)

# Save the original sample data
data.to_csv("data/raw/developer_activity.csv", index=False)

# Validate and clean the data
data = data.drop_duplicates()
data = data.dropna()

data["date"] = pd.to_datetime(data["date"])
data["focus_score"] = data["focus_score"].clip(0, 100)
data["cognitive_load_score"] = data["cognitive_load_score"].clip(0, 100)

# Add focus categories
data["focus_category"] = pd.cut(
    data["focus_score"],
    bins=[-1, 49, 74, 100],
    labels=["Low", "Medium", "High"]
)

# Save processed data
data.to_csv("data/processed/developer_activity_cleaned.csv", index=False)

# Generate summary statistics
summary = data.describe(include="all").transpose()
summary.to_csv("results/summary_statistics.csv")

# Calculate key performance indicators
kpis = pd.DataFrame({
    "Metric": [
        "Total Sessions",
        "Unique Developers",
        "Average Focus Score",
        "Average Cognitive Load",
        "Average Interruptions",
        "Total Tasks Completed",
    ],
    "Value": [
        len(data),
        data["developer_id"].nunique(),
        round(data["focus_score"].mean(), 2),
        round(data["cognitive_load_score"].mean(), 2),
        round(data["interruptions"].mean(), 2),
        int(data["tasks_completed"].sum()),
    ]
})

kpis.to_csv("results/kpi_summary.csv", index=False)

print("CogniStream analysis completed successfully!")
print("\nDataset shape:", data.shape)
print("\nKey Performance Indicators:")
print(kpis.to_string(index=False))
print("\nFiles created:")
print("- data/raw/developer_activity.csv")
print("- data/processed/developer_activity_cleaned.csv")
print("- results/summary_statistics.csv")
print("- results/kpi_summary.csv")