from pathlib import Path
import sqlite3
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.data_processing import load_and_normalize

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "transport_analytics.db"
AGENCIES = {
    "MARTA": ("Metropolitan Atlanta Rapid Transit Authority", "Atlanta, Georgia, USA"),
    "TRIMET": ("Tri-County Metropolitan Transportation District of Oregon", "Portland, Oregon, USA"),
    "MIAMI_DADE": ("Miami-Dade Transit", "Miami-Dade, Florida, USA"),
    "METRO_TRANSIT": ("Metro Transit", "Minneapolis–Saint Paul, Minnesota, USA"),
}

def main():
    df = load_and_normalize(ROOT / "data" / "raw")
    con = sqlite3.connect(DB)
    con.executescript((ROOT / "database" / "schema.sql").read_text(encoding="utf-8"))
    for code, (name, region) in AGENCIES.items():
        con.execute("INSERT OR IGNORE INTO agency(agency_code,agency_name,city_region) VALUES(?,?,?)", (code,name,region))
    for _, r in df.iterrows():
        agency_id = con.execute("SELECT agency_id FROM agency WHERE agency_code=?", (r.agency,)).fetchone()[0]
        con.execute("INSERT OR IGNORE INTO route(agency_id,source_route_id) VALUES(?,?)", (agency_id,r.route_id))
        route_pk = con.execute("SELECT route_pk FROM route WHERE agency_id=? AND source_route_id=?", (agency_id,r.route_id)).fetchone()[0]
        con.execute("""INSERT OR REPLACE INTO route_period
            (route_pk,period_code,summary_begin_date,stops,avg_on_per_trip,avg_trips,sum_ons,avg_ons,source_file)
            VALUES(?,?,?,?,?,?,?,?,?)""",
            (route_pk,r.period_code,r.summary_begin_date,
             None if r.stops != r.stops else float(r.stops),
             None if r.avg_on_per_trip != r.avg_on_per_trip else float(r.avg_on_per_trip),
             None if r.avg_trips != r.avg_trips else float(r.avg_trips),
             None if r.sum_ons != r.sum_ons else float(r.sum_ons),
             None if r.avg_ons != r.avg_ons else float(r.avg_ons),r.source_file))
    con.commit()
    counts = con.execute("SELECT (SELECT COUNT(*) FROM agency),(SELECT COUNT(*) FROM route),(SELECT COUNT(*) FROM route_period)").fetchone()
    con.close()
    print(f"Database tayyor: {DB}\nAgency={counts[0]}, route={counts[1]}, route_period={counts[2]}")

if __name__ == "__main__": main()
