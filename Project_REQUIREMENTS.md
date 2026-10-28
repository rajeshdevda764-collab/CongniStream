# CogniStream: Developer Flow-State & Cognitive Load Analytics

## 1. Project Overview

CogniStream is a data analytics application designed to analyze developer work patterns, estimate cognitive workload, and identify conditions associated with productive, focused work sessions.

## 2. Project Objectives

- Collect and organize developer work-session data.
- Clean and validate datasets using Python and Pandas.
- Analyze focus time, interruptions, task complexity, and productivity.
- Estimate cognitive load and flow-state indicators.
- Identify patterns and trends across work sessions.
- Develop an interactive dashboard using Streamlit.
- Generate understandable insights and recommendations.

## 3. Technology Stack

- **Programming Language:** Python
- **Data Processing:** Pandas and NumPy
- **Visualization:** Plotly
- **Dashboard:** Streamlit
- **Version Control:** Git and GitHub
- **Development Environment:** Visual Studio Code

## 4. Proposed Dataset Structure

The dataset will contain the following columns:

| Column | Description |
|---|---|
| session_id | Unique work-session identifier |
| developer_id | Anonymous developer identifier |
| date | Date of the work session |
| task_type | Type of development activity |
| session_duration_min | Total session duration in minutes |
| focused_time_min | Time spent focusing |
| interruptions | Number of interruptions |
| task_complexity | Task difficulty from 1 to 5 |
| perceived_workload | Self-reported workload from 1 to 5 |
| completed_tasks | Number of completed tasks |
| productivity_score | Estimated productivity metric |

## 5. Proposed System Modules

1. Data Collection and Validation
2. Data Cleaning and Preprocessing
3. Exploratory Data Analysis
4. Cognitive Load Analysis
5. Flow-State Scoring
6. Interactive Analytics Dashboard
7. Insights and Reporting

## 6. Expected Dashboard Features

- Developer and date filters
- Focus-time analysis
- Interruption statistics
- Productivity trends
- Cognitive load indicators
- Flow-state analytics
- Interactive charts
- Summary insights

## 7. Data Source

The initial implementation will use a synthetic developer work-session dataset for educational analytics. Synthetic records will be clearly identified as simulated rather than real employee observations.

## 8. Expected Outcome

A functioning analytics application capable of processing developer work-session data, presenting interactive visualizations, and highlighting trends related to developer focus, cognitive workload, and productivity.

Flow-state and cognitive-load metrics will be estimates based on defined indicators, not clinical or validated psychological measurements.