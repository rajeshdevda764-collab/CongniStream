# CogniStream — Completion Add-on

**Project:** CogniStream: Developer Flow-State & Cognitive Load Analytics  
**Internship:** Infotact Solutions — Data Analytics  
**Data:** Synthetic work sessions (demo), not real employee telemetry.

## Installation into your existing CogniStream repository

1. Extract this ZIP.
2. Copy `dashboard/`, `tests/`, `docs/`, `run_dashboard.bat`, `run_tests.bat`, and `requirements-completion.txt` into the **root** of your existing CogniStream repository. Do not delete your existing `src/`, `data/`, `reports/`, `README.md`, `.git`, or Power BI `.pbix` file.
3. You must retain your existing `data/processed/flow_state_results.csv` (generated on Day 9). Do not rename it.
4. In the root of the repository, run:

   ```cmd
   .venv\Scripts\activate
   python -m pip install -r requirements-completion.txt
   python -m pytest tests -q
   python -m streamlit run dashboard\app.py
   ```

5. The local Streamlit URL shown in your terminal (typically `http://localhost:8501`) opens the dashboard. The dashboard starts with all developers and task types selected. Test the filters and the filtered-data CSV export.
6. Open `CogniStream_Mid_Review.pbix` separately in **Power BI Desktop**. The PBIX is not modified by this add-on.

## Features

- Overall KPI metrics: number of sessions, productivity, estimated cognitive load, estimated flow state, focus efficiency
- Sidebar filters for developer, task, date range and flow category
- Flow distribution, productivity comparison, cognitive-load doughnut, time trend
- Load–productivity scatter plot, flow gauge, developer × task heatmap and interruption trend
- Session explorer and filtered CSV export
- Data validation for required fields, duplicate IDs and impossible focus durations
- Basic automated data-contract tests

## Metric definitions

- Focus efficiency = total focused minutes / total session minutes.
- Cognitive load = 0.40 × normalized complexity + 0.30 × normalized interruptions + 0.30 × normalized synthetic workload.
- Flow = 0.60 × session focus percentage + 0.25 × interruption score + 0.15 × load balance. Load balance peaks at 50.
- Thresholds: cognitive load Low <35; Moderate 35–<70; High >=70. Flow Low <40; Moderate 40–<70; High >=70.

**Important:** Scores are pedagogical heuristics, not validated cognitive or flow measurements. Generator-defined relationships are not real-world empirical effects.

## Suggested Git steps (only after testing)

```cmd
git status
git add dashboard tests docs README_COMPLETION.md requirements-completion.txt run_dashboard.bat run_tests.bat
git commit -m "Final: Add CogniStream dashboard tests and documentation"
git push origin main
```

Do not copy the ZIP itself into Git unless desired. Do not change existing commit history. For final deliverables, include the source repo, the PBIX file, final presentation, report, and a live demonstration.
