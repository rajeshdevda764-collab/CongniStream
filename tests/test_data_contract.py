"""Sanity tests for the actual processed dataset, independent of Streamlit."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FILE = ROOT / 'data' / 'processed' / 'flow_state_results.csv'

def test_data_contract():
    assert FILE.exists(), f'Missing expected file: {FILE}'
    df = pd.read_csv(FILE)
    fields = {'session_id','developer_id','date','task_type','session_duration_min','focused_time_min','productivity_score','cognitive_load_score','flow_state_score','flow_state_level'}
    assert not fields.difference(df.columns), f'Missing: {fields.difference(df.columns)}'
    assert not df.empty
    assert df.session_id.is_unique
    assert (df.session_duration_min>0).all()
    assert df.focused_time_min.between(0,df.session_duration_min).all()
    assert df.productivity_score.between(0,100).all()
    assert df.cognitive_load_score.between(0,100).all()
    assert df.flow_state_score.between(0,100).all()
    assert df.flow_state_level.isin(['Low Flow','Moderate Flow','High Flow']).all()

def test_dashboard_source_exists():
    assert (ROOT/'dashboard'/'app.py').exists()
