import os
import pandas as pd
import matplotlib.pyplot as plt

# Create output folder
os.makedirs("charts", exist_ok=True)

# Load cleaned dataset
file_path = "data/processed/developer_activity_cleaned.csv"
df = pd.read_csv(file_path)

# Chart 1: Focus score distribution
plt.figure(figsize=(9, 5))
plt.hist(df["focus_score"], bins=15, edgecolor="black")
plt.title("Developer Focus Score Distribution")
plt.xlabel("Focus Score")
plt.ylabel("Number of Sessions")
plt.tight_layout()
plt.savefig("charts/focus_distribution.png", dpi=150)
plt.close()

# Chart 2: Cognitive load distribution
plt.figure(figsize=(9, 5))
plt.hist(df["cognitive_load_score"], bins=15, edgecolor="black")
plt.title("Cognitive Load Score Distribution")
plt.xlabel("Cognitive Load Score")
plt.ylabel("Number of Sessions")
plt.tight_layout()
plt.savefig("charts/cognitive_load_distribution.png", dpi=150)
plt.close()

# Chart 3: Average focus score by developer
developer_focus = df.groupby("developer_id")["focus_score"].mean().sort_index()

plt.figure(figsize=(11, 5))
developer_focus.plot(kind="bar")
plt.title("Average Focus Score by Developer")
plt.xlabel("Developer ID")
plt.ylabel("Average Focus Score")
plt.tight_layout()
plt.savefig("charts/focus_by_developer.png", dpi=150)
plt.close()

# Chart 4: Interruptions vs cognitive load
plt.figure(figsize=(9, 5))
plt.scatter(df["interruptions"], df["cognitive_load_score"], alpha=0.5)
plt.title("Interruptions vs Cognitive Load")
plt.xlabel("Number of Interruptions")
plt.ylabel("Cognitive Load Score")
plt.tight_layout()
plt.savefig("charts/interruptions_vs_load.png", dpi=150)
plt.close()

print("All 4 charts created successfully!")
print("Check the charts folder for PNG files.")