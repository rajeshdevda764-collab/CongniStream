
import csv
import random
from datetime import date, timedelta
from pathlib import Path

# CogniStream - Day 3
# Synthetic developer work-session dataset

rng = random.Random(42)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = PROJECT_ROOT / "data" / "developer_sessions.csv"

NUM_SESSIONS = 500
NUM_DEVELOPERS = 10

task_types = [
    "Coding",
    "Debugging",
    "Testing",
    "Code Review",
    "Documentation",
    "Planning"
]

start_date = date(2026, 9, 1)
end_date = date(2026, 10, 28)
total_days = (end_date - start_date).days

records = []

for i in range(1, NUM_SESSIONS + 1):
    developer_id = f"DEV{rng.randint(1, NUM_DEVELOPERS):03d}"
    session_date = start_date + timedelta(
        days=rng.randint(0, total_days)
    )

    task_type = rng.choice(task_types)
    session_duration = rng.randint(60, 240)
    task_complexity = rng.randint(1, 5)
    interruptions = rng.randint(0, 10)

    # Simulated focus-time estimate
    focus_ratio = (
        0.90
        - interruptions * 0.035
        - task_complexity * 0.015
        + rng.uniform(-0.08, 0.08)
    )
    focus_ratio = max(0.25, min(0.95, focus_ratio))
    focused_time = round(session_duration * focus_ratio)

    # Simulated workload estimate (not a real self-report)
    perceived_workload = round(
        max(1, min(
            5,
            task_complexity * 0.65
            + interruptions * 0.18
            + rng.uniform(0, 1.5)
        ))
    )

    completed_tasks = max(
        0,
        round(
            focused_time / (35 + task_complexity * 12)
            + rng.uniform(-0.5, 1.5)
        )
    )

    # Synthetic productivity score from 0 to 100
    productivity_score = round(
        max(0, min(
            100,
            100 * focus_ratio
            - interruptions * 1.5
            + completed_tasks * 3
            + rng.uniform(-5, 5)
        )),
        2
    )

    records.append({
        "session_id": f"SES{i:04d}",
        "developer_id": developer_id,
        "date": session_date.isoformat(),
        "task_type": task_type,
        "session_duration_min": session_duration,
        "focused_time_min": focused_time,
        "interruptions": interruptions,
        "task_complexity": task_complexity,
        "perceived_workload": perceived_workload,
        "completed_tasks": completed_tasks,
        "productivity_score": productivity_score
    })

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=records[0].keys())
    writer.writeheader()
    writer.writerows(records)

assert len(records) == NUM_SESSIONS
assert len({r["session_id"] for r in records}) == NUM_SESSIONS
assert all(
    0 <= r["focused_time_min"] <= r["session_duration_min"]
    and 0 <= r["productivity_score"] <= 100
    and 1 <= r["perceived_workload"] <= 5
    for r in records
)

print("CogniStream dataset generated successfully!")
print(f"Total Sessions: {len(records)}")
print(f"Total Developers: {NUM_DEVELOPERS}")
print(f"Saved to: {OUTPUT_FILE}")
