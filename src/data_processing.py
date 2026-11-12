from pathlib import Path
import pandas as pd

FILES = {
    "MARTA": "MARTA_Route.csv",
    "TRIMET": "TRIMET_Route.csv",
    "MIAMI_DADE": "MIAMI_DADE_Route.csv",
    "METRO_TRANSIT": "METRO_TRANSIT_Route.csv",
}
ID_COLUMNS = {
    "MARTA": "route_id",
    "TRIMET": "route_number",
    "MIAMI_DADE": "QSTOPROUTE",
    "METRO_TRANSIT": "line_id",
}
METRICS = ["Stops", "AVGonPERtrip", "AVGtrips", "SUMons", "AVGons"]
CANONICAL = {"Stops":"stops", "AVGonPERtrip":"avg_on_per_trip", "AVGtrips":"avg_trips", "SUMons":"sum_ons", "AVGons":"avg_ons"}


def load_and_normalize(data_dir="data/raw"):
    """Load source CSVs and normalize wide period-suffixed columns to long form.

    The source's 12/17 suffixes are retained as period codes. They are not
    blindly treated as calendar years because agencies have different markup dates.
    """
    data_dir = Path(data_dir)
    frames = []
    for agency, filename in FILES.items():
        path = data_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Dataset fayli topilmadi: {path}")
        raw = pd.read_csv(path)
        id_col = ID_COLUMNS[agency]
        required = [id_col, "summary_begin_date12", "summary_begin_date17"]
        missing = [c for c in required if c not in raw.columns]
        if missing:
            raise ValueError(f"{filename}: kerakli ustunlar yo'q: {missing}")
        raw = raw.drop(columns=[c for c in raw.columns if c.lower().startswith("unnamed")], errors="ignore")
        raw = raw.rename(columns={id_col: "route_id"})
        raw["route_id"] = raw["route_id"].astype(str).str.strip()
        raw["agency"] = agency
        raw["source_file"] = filename
        for suffix in ("12", "17"):
            date_col = f"summary_begin_date{suffix}"
            part = pd.DataFrame({
                "agency": raw["agency"],
                "route_id": raw["route_id"],
                "period_code": suffix,
                "summary_begin_date": raw[date_col].astype(str),
                "source_file": raw["source_file"],
            })
            for metric in METRICS:
                col = f"{metric}{suffix}"
                if col not in raw.columns:
                    raise ValueError(f"{filename}: {col} ustuni topilmadi")
                part[CANONICAL[metric]] = pd.to_numeric(raw[col], errors="coerce")
            frames.append(part)
    result = pd.concat(frames, ignore_index=True)
    numeric = list(CANONICAL.values())
    # Keep rows, but reject impossible negative values as invalid rather than silently changing them.
    if (result[numeric] < 0).any().any():
        raise ValueError("Datasetda manfiy metrik qiymatlar topildi; tekshiruv talab qilinadi.")
    return result


def quality_report(data_dir="data/raw"):
    rows = []
    for agency, filename in FILES.items():
        df = pd.read_csv(Path(data_dir) / filename)
        rows.append({
            "agency": agency,
            "file": filename,
            "rows": len(df),
            "columns": len(df.columns),
            "missing_cells": int(df.isna().sum().sum()),
            "duplicate_rows": int(df.duplicated().sum()),
            "unique_routes": int(df[ID_COLUMNS[agency]].nunique()),
        })
    return pd.DataFrame(rows)
