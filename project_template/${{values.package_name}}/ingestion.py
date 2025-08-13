from __future__ import annotations
from pathlib import Path
import pandas as pd

def load_table(path: str | Path) -> pd.DataFrame:
    """Load CSV or Parquet into a DataFrame with standardised dtypes."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)
    if p.suffix.lower() in {".csv"}:
        df = pd.read_csv(p)
    elif p.suffix.lower() in {".parquet", ".pq"}:
        df = pd.read_parquet(p)
    else:
        raise ValueError(f"Unsupported file type: {p.suffix}")
    # Normalise column names
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return df
