from __future__ import annotations
import math
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def primary_suppression(df: pd.DataFrame, threshold: int) -> pd.DataFrame:
    """Suppress rows with n < threshold by setting sensitive cells to NaN."""
    out = df.copy()
    mask = out["n"] < threshold
    suppressed_count = mask.sum()
    logging.info(f"Applying primary suppression: threshold={threshold}, suppressed rows={suppressed_count}")
    for col in ("total", "mean"):
        if col in out.columns:
            out.loc[mask, col] = pd.NA
            logging.debug(f"Suppressed column '{col}' for {suppressed_count} rows.")
    out.loc[mask, "suppressed"] = True
    out.loc[~mask, "suppressed"] = False
    return out

def rounding(df: pd.DataFrame, base: int) -> pd.DataFrame:
    """Round publishable numeric cells to the nearest 'base'."""
    out = df.copy()
    logging.info(f"Applying rounding: base={base}")
    for col in ("total", "mean"):
        if col in out.columns:
            before = out[col].copy()
            out[col] = out[col].apply(
                lambda x: (math.floor((x / base) + 0.5) * base) if pd.notna(x) else x
            )
            changed = (before != out[col]).sum()
            logging.debug(f"Rounded column '{col}' for {changed} rows.")
    return out
