# CogniStream: Developer Flow-State & Cognitive Load Analytics

## Project Report — Completion Draft

**Internship Organization:** Infotact Solutions  
**Domain:** Data Analytics  
**Project period stated in assignment letter:** 12 October – 12 November 2026  
**Project type:** Synthetic demonstration analytics application

## Abstract
CogniStream demonstrates a reproducible data analytics workflow for simulated developer work sessions. Python is used to generate, inspect, clean and analyze data, and to derive indicative productivity, cognitive-load and flow-state scores. A Power BI report and a Streamlit dashboard visualize the simulated sessions with interactive filters. The metrics are heuristics designed for learning, not verified measures of employees' cognitive state or productivity.

## 1. Problem statement
Developer work patterns involve tasks of varying complexity, interruptions and periods of focused activity. This project explores how those factors can be organized, visualized and compared using a simulated dataset. It is an educational analytics demonstration, not a monitoring or employee-ranking tool.

## 2. Objectives
- Structure and validate developer session records
- Analyze distributions of session time, focus, interruptions and task categories
- Calculate transparent, interpretable heuristic scores
- Build interactive visualizations and demonstrate filtering
- Produce documented, reproducible outputs and verify core data rules

## 3. Dataset
The synthetic dataset contains **500 work sessions**, **10 anonymous developer IDs**, and six task categories: Planning, Documentation, Code Review, Debugging, Coding and Testing. Original fields include session ID, developer ID, date, task type, session duration, focused time, interruption count, task complexity, simulated perceived workload, completed tasks, and a synthetic productivity score.

## 4. Tools
Python, pandas, NumPy, Matplotlib, Plotly, Streamlit, Power BI Desktop, Git and GitHub.

## 5. Implementation
1. **Generation:** deterministic synthetic session generator.
2. **Inspection:** check rows, columns, missing values, types and duplicates.
3. **Cleaning:** validate required fields, numeric ranges and unique session IDs; output processed CSV.
4. **Exploratory analysis:** charts of task distribution, focus time, interruptions and task complexity.
5. **Productivity analysis:** per-developer aggregates of work and focused time, tasks and synthetic productivity.
6. **Cognitive load:** weighted heuristic over normalized complexity, interruption count and simulated workload.
7. **Flow-state scoring:** weighted heuristic over focus ratio, interruption score and workload balance.
8. **Visualization:** interactive Power BI report and optional Streamlit dashboard.
9. **Validation:** required-column checks, unique sessions, score bounds and focused-time rules.

## 6. Summary results (reported in development logs)

| Metric | Result |
|---|---:|
| Sessions | 500 |
| Anonymous developers | 10 |
| Mean focused time | 104.41 minutes |
| Mean simulated productivity score | 66.86 / 100 |
| Mean interruption count | 4.91 |
| Mean focus ratio (unweighted across sessions) | 67.81% |
| Weighted focus efficiency | 67.86% |
| Mean estimated cognitive load | 55.18 / 100 |
| Mean estimated flow score | 61.97 / 100 |
| Cognitive load: low / moderate / high | 111 / 229 / 160 |
| Flow: low / moderate / high | 53 / 272 / 175 |

These figures came from the user's terminal logs and should be checked again in the final dashboard after any dataset changes.

## 7. Visualizations
The Power BI report includes KPI calculations, developer productivity and flow-state charts, and slicers for developer and task type. The completion Streamlit dashboard also presents an interactive load–productivity scatter plot, flow gauge, developer × task heatmap, load donut and time trends.

## 8. Limitations
- All session data is artificially generated and cannot establish real-world causal relationships.
- The productivity formula used in data generation includes interruptions, making some correlations expected by design.
- Cognitive-load and flow-state scores are unvalidated teaching heuristics with arbitrarily selected weights and thresholds.
- The application must not be used for personnel decisions or health assessment.
- Additional real data, appropriate consent and rigorous metric validation would be necessary before any operational deployment.

## 9. Conclusion
CogniStream demonstrates a complete educational analytics workflow from data ingestion and cleaning through statistical summaries, transparent derived features and interactive dashboard visualization. The platform illustrates how filters and structured data can help users explore patterns in a controlled synthetic dataset.

## References and further reading
- Python documentation: https://docs.python.org/3/
- pandas documentation: https://pandas.pydata.org/docs/
- Plotly documentation: https://plotly.com/python/
- Streamlit documentation: https://docs.streamlit.io/
- Microsoft Power BI documentation: https://learn.microsoft.com/power-bi/

## Submission verification checklist
- [ ] Confirm application starts and all tabs render
- [ ] Confirm filters, chart tooltips and CSV download work
- [ ] Run tests against existing Day 9 dataset
- [ ] Open and save PBIX; ensure full dataset selected
- [ ] Update final report with screenshots and exact run date
- [ ] Demonstrate live app and Power BI dashboard
- [ ] Commit and push final changes
