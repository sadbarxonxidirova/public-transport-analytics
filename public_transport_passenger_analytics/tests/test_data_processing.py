from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data_processing import load_and_normalize, quality_report

ROOT=Path(__file__).resolve().parents[1]

def test_all_agencies_loaded():
    df=load_and_normalize(ROOT/"data"/"raw")
    assert set(df.agency)=={"MARTA","TRIMET","MIAMI_DADE","METRO_TRANSIT"}
    assert len(df)==716

def test_periods_and_nonnegative_metrics():
    df=load_and_normalize(ROOT/"data"/"raw")
    assert set(df.period_code)=={"12","17"}
    assert (df[["stops","avg_on_per_trip","avg_trips","sum_ons","avg_ons"]]>=0).all().all()

def test_source_quality():
    q=quality_report(ROOT/"data"/"raw")
    assert q.rows.sum()==358
    assert q.missing_cells.sum()==0
    assert q.duplicate_rows.sum()==0
