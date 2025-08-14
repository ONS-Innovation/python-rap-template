from __future__ import annotations
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

def load_table(path: str | Path) -> pd.DataFrame:
    """Load CSV or Parquet into a DataFrame with standardised dtypes."""
    p = Path(path)
    logger.info(f"Loading data from: {p}")
    if not p.exists():
        logger.error(f"File not found: {p}")
        raise FileNotFoundError(p)
    if p.suffix.lower() in {".csv"}:
        df = pd.read_csv(p)
        logger.info(f"Loaded CSV file with shape: {df.shape}")
    elif p.suffix.lower() in {".parquet", ".pq"}:
        df = pd.read_parquet(p)
        logger.info(f"Loaded Parquet file with shape: {df.shape}")
    else:
        logger.error(f"Unsupported file type: {p.suffix}")
        raise ValueError(f"Unsupported file type: {p.suffix}")
    # Normalise column names
    old_columns = list(df.columns)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
    logger.debug(f"Normalized columns from {old_columns} to {list(df.columns)}")
    return df
