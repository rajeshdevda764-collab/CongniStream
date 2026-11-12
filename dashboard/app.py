"""CogniStream interactive analytics dashboard.
Run at repository root: streamlit run dashboard/app.py
All metrics are illustrative; records are synthetic.
"""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / 'data' / 'processed'
CANDIDATES = [DATA_DIR / 'flow_state_results.csv', DATA_DIR / 'cognitive_load_results.csv', DATA_DIR / 'developer_sessions_cleaned.csv']
COLORS = {'Low Flow':'#e5a971','Moderate Flow':'#75b6e7','High Flow':'#4cceb0'}

st.set_page_config(page_title='CogniStream | Developer Analytics', page_icon='🧠', layout='wide')
if st.sidebar.button("🔄 Refresh Dashboard"):
    st.cache_data.clear()
    st.rerun()
st.markdown('''<style>
.stApp{background:#0a1425;color:#eaf1fc}
[data-testid="stMetric"]{background:#152641;border:1px solid #28415d;border-radius:14px;padding:16px}
h1,h2,h3{color:#eaf1fc!important}
</style>''',unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {'session_id','developer_id','date','task_type','session_duration_min','focused_time_min','interruptions','task_complexity','productivity_score'}
    missing=required.difference(df.columns)
    if missing: raise ValueError(f'Missing required columns: {sorted(missing)}')
    if df['session_id'].duplicated().any(): raise ValueError('Duplicate session IDs detected')
    df['date']=pd.to_datetime(df['date'],errors='coerce')
    if df['date'].isna().any(): raise ValueError('Invalid dates detected')
    duration=pd.to_numeric(df['session_duration_min'],errors='coerce')
    focused=pd.to_numeric(df['focused_time_min'],errors='coerce')
    if (duration<=0).any() or (focused<0).any() or (focused>duration).any():
        raise ValueError('Invalid focused/session duration')
    df['focus_ratio']=(focused/duration)
    # Reproduce the explicitly stated Day 8 and Day 9 heuristic formulas
    if 'cognitive_load_score' not in df.columns:
        if 'perceived_workload' not in df.columns:
            raise ValueError('Missing perceived_workload required to derive the cognitive load score')
        df['cognitive_load_score']=(.4*((df.task_complexity-1)/4*100)+.3*(df.interruptions/10*100)+.3*((df.perceived_workload-1)/4*100)).round(2)
    if 'cognitive_load_level' not in df.columns:
        df['cognitive_load_level']=pd.cut(df.cognitive_load_score,[-float('inf'),35,70,float('inf')],right=False,labels=['Low','Moderate','High']).astype(str)
    if 'flow_state_score' not in df.columns:
        balance=(100-2*(df.cognitive_load_score-50).abs()).clip(0,100)
        df['flow_state_score']=(.60*(df.focus_ratio*100)+.25*(100-df.interruptions*10)+.15*balance).round(2)
    if 'flow_state_level' not in df.columns:
        df['flow_state_level']=pd.cut(df.flow_state_score,[-float('inf'),40,70,float('inf')],right=False,labels=['Low Flow','Moderate Flow','High Flow']).astype(str)
    return df

available=next((p for p in CANDIDATES if p.exists()),None)
if available is None:
    st.error('Dataset not found. Copy your existing CSV into data/processed/flow_state_results.csv (preferred) or developer_sessions_cleaned.csv.')
    st.code('streamlit run dashboard/app.py')
    st.stop()
try:
    all_df=load_data(str(available))
except (ValueError,KeyError,TypeError) as ex:
    st.error(f'Dataset validation failed: {ex}')
    st.stop()

st.title('COGNISTREAM')
st.caption('Developer Flow-State & Cognitive Load Analytics | Infotact Solutions | Synthetic demonstration data')

# Day 13: Reset dashboard filters
if st.session_state.pop("reset_filters", False):
    for key in ["filter_devs", "filter_tasks", "filter_dates", "filter_flows"]:
        st.session_state.pop(key, None)

# Day 13: Reset dashboard filters
if st.session_state.pop("reset_filters", False):
    for key in ["filter_devs", "filter_tasks", "filter_dates", "filter_flows"]:
        st.session_state.pop(key, None)

# Day 13: Reset dashboard filters
if st.session_state.pop("reset_filters", False):
    for key in ["filter_devs", "filter_tasks", "filter_dates", "filter_flows"]:
        st.session_state.pop(key, None)
with st.sidebar:
 
    st.header('Explore sessions')
    devs=st.multiselect('Developers', sorted(all_df.developer_id.unique()),default=sorted(all_df.developer_id.unique()))
    tasks=st.multiselect('Task types',sorted(all_df.task_type.unique()),default=sorted(all_df.task_type.unique()))
    lo,hi=all_df.date.min().date(),all_df.date.max().date()
    dates=st.date_input('Date range',value=(lo,hi),min_value=lo,max_value=hi)
    flows=st.multiselect('Flow states',['Low Flow','Moderate Flow','High Flow'],default=['Low Flow','Moderate Flow','High Flow'])
    st.caption('Source: '+available.name)

df=all_df[all_df.developer_id.isin(devs)&all_df.task_type.isin(tasks)&all_df.flow_state_level.isin(flows)].copy()
if isinstance(dates,(tuple,list)) and len(dates)==2:
    df=df[df.date.dt.date.between(dates[0],dates[1])]
if df.empty:
    st.warning('No sessions match the current filters. Try resetting the sidebar selections.')
    st.stop()

k1,k2,k3,k4,k5=st.columns(5)
k1.metric('Sessions',f'{len(df):,}')
k2.metric('Avg productivity',f'{df.productivity_score.mean():.2f}/100')
k3.metric('Estimated cognitive load',f'{df.cognitive_load_score.mean():.2f}/100')
k4.metric('Estimated flow',f'{df.flow_state_score.mean():.2f}/100')
k5.metric('Focus efficiency',f'{df.focused_time_min.sum()/df.session_duration_min.sum():.1%}')

overview,analysis,detail=st.tabs(['Overview','Advanced Analytics','Session Explorer'])
plot_layout=dict(template='plotly_dark',paper_bgcolor='#101e33',plot_bgcolor='#101e33',font_color='#eaf1fc')
with overview:
    left,right=st.columns(2)
    counts=df.flow_state_level.value_counts().reindex(['Low Flow','Moderate Flow','High Flow'],fill_value=0).rename_axis('Flow level').reset_index(name='Sessions')
    fig=px.bar(counts,x='Flow level',y='Sessions',color='Flow level',color_discrete_map=COLORS,title='Estimated Flow-State Distribution')
    fig.update_layout(**plot_layout,showlegend=False)
    left.plotly_chart(fig,use_container_width=True)
    sums=df.groupby('developer_id',as_index=False).agg(productivity=('productivity_score','mean')).sort_values('productivity',ascending=True)
    fig=px.bar(sums,x='productivity',y='developer_id',orientation='h',title='Average Simulated Productivity by Developer',labels={'productivity':'Avg score','developer_id':'Developer'})
    fig.update_layout(**plot_layout,xaxis_range=[0,100])
    right.plotly_chart(fig,use_container_width=True)
    left,right=st.columns(2)
    load=df.cognitive_load_level.value_counts().reindex(['Low','Moderate','High'],fill_value=0).rename_axis('Load level').reset_index(name='Sessions')
    fig=px.pie(load,names='Load level',values='Sessions',hole=.57,title='Estimated Cognitive Load Categories')
    fig.update_layout(**plot_layout)
    left.plotly_chart(fig,use_container_width=True)
    trend=df.groupby(df.date.dt.date,as_index=False).agg(flow_state_score=('flow_state_score','mean'))
    fig=px.line(trend,x='date',y='flow_state_score',markers=True,title='Estimated Flow Score by Date',labels={'date':'Date','flow_state_score':'Avg flow score'})
    fig.update_layout(**plot_layout,yaxis_range=[0,100])
    right.plotly_chart(fig,use_container_width=True)
with analysis:
    left,right=st.columns(2)
    fig=px.scatter(df,x='cognitive_load_score',y='productivity_score',color='flow_state_level',hover_data=['session_id','developer_id','task_type','interruptions'],color_discrete_map=COLORS,title='Cognitive Load vs Productivity',labels={'cognitive_load_score':'Estimated load','productivity_score':'Simulated productivity'})
    fig.update_layout(**plot_layout,xaxis_range=[0,100],yaxis_range=[0,100])
    left.plotly_chart(fig,use_container_width=True)
    fig=go.Figure(go.Indicator(mode='gauge+number',value=float(df.flow_state_score.mean()),title={'text':'Average Estimated Flow Score'},gauge={'axis':{'range':[0,100]},'bar':{'color':'#47cdb2'},'steps':[{'range':[0,40],'color':'#46394b'},{'range':[40,70],'color':'#254d68'},{'range':[70,100],'color':'#225f58'}]}))
    fig.update_layout(**plot_layout)
    right.plotly_chart(fig,use_container_width=True)
    pivot=df.pivot_table(index='developer_id',columns='task_type',values='productivity_score',aggfunc='mean')
    fig=px.imshow(pivot,aspect='auto',color_continuous_scale='Tealgrn',title='Developer × Task Productivity Heatmap',labels={'color':'Avg score'})
    fig.update_layout(**plot_layout)
    st.plotly_chart(fig,use_container_width=True)
    interrupted=df.groupby('interruptions',as_index=False).agg(average_productivity=('productivity_score','mean'),sessions=('session_id','count'))
    fig=px.line(interrupted,x='interruptions',y='average_productivity',markers=True,title='Average Productivity by Interruption Count',hover_data=['sessions'])
    fig.update_layout(**plot_layout,yaxis_range=[0,100])
    st.plotly_chart(fig,use_container_width=True)
with detail:
    st.subheader('Filtered sessions')
    st.dataframe(df.sort_values('date',ascending=False),use_container_width=True,hide_index=True)
    st.download_button('Download filtered CSV',df.to_csv(index=False).encode('utf-8'),'cognistream_filtered.csv','text/csv')

st.divider()
st.caption('Methodology: synthetic data. Cognitive load (40% complexity, 30% interruptions, 30% simulated workload) and flow state (60% focus, 25% interruptions, 15% load balance) are unvalidated heuristic scores. They are not real-world psychological or employee performance measurements. Correlations in generated data do not establish causal relationships.')


# Day 14: Developer Comparison Insights
st.subheader("Developer Comparison Insights")

developer_comparison = (
    df.groupby("developer_id", as_index=False)
    .agg(
        avg_productivity=("productivity_score", "mean"),
        avg_cognitive_load=("cognitive_load_score", "mean"),
        avg_flow_score=("flow_state_score", "mean"),
        sessions=("session_id", "count"),
    )
    .round(2)
)

st.dataframe(
    developer_comparison,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Compare productivity, estimated cognitive load, "
    "and flow-state scores across developers."
)


# Day 15: Cognitive Load Distribution
st.subheader("Cognitive Load Distribution")

if "cognitive_load_level" in df.columns:
    load_counts = (
        df["cognitive_load_level"]
        .value_counts()
        .reindex(["Low", "Moderate", "High"], fill_value=0)
    )

    st.bar_chart(load_counts)
else:
    st.info("Cognitive load categories are not available.")


# Day 16: Flow-State Trend Analysis
st.subheader("Daily Flow-State Trend")

flow_trend = (
    df.groupby(df["date"].dt.date)["flow_state_score"]
    .mean()
    .reset_index()
)

flow_trend.columns = ["Date", "Average Flow Score"]

st.line_chart(
    flow_trend,
    x="Date",
    y="Average Flow Score"
)

st.caption(
    "Daily average estimated flow-state score "
    "across selected developer sessions."
)

# Day 17: Productivity Recommendations
st.subheader("Productivity Recommendations")

avg_productivity = df["productivity_score"].mean()
avg_interruptions = df["interruptions"].mean()

if avg_interruptions >= 6:
    st.info(
        "High interruption levels detected. "
        "Consider reducing unnecessary notifications "
        "and scheduling focused work periods."
    )
else:
    st.success(
        "Interruption levels are relatively low. "
        "Continue supporting distraction-free work."
    )

if avg_productivity < 60:
    st.warning(
        "Average productivity is below 60. "
        "Consider reviewing task priorities and "
        "workload distribution."
    )
else:
    st.info(
        "Average productivity is 60 or above. "
        "Continue monitoring trends and improving workflows."
    )

st.caption(
    "Recommendations are based on simulated session data "
    "and simple thresholds, not individual performance assessments."
)
