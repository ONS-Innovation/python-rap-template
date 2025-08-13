from __future__ import annotations
import math
import pandas as pd

def primary_suppression(df: pd.DataFrame, threshold: int) -> pd.DataFrame:
    """Suppress rows with n < threshold by setting sensitive cells to NaN."""
    out = df.copy()
    mask = out["n"] < threshold
    for col in ("total", "mean"):
        if col in out.columns:
            out.loc[mask, col] = pd.NA
    out.loc[mask, "suppressed"] = True
    out.loc[~mask, "suppressed"] = False
    return out

def rounding(df: pd.DataFrame, base: int) -> pd.DataFrame:
    """Round publishable numeric cells to the nearest 'base'."""
    out = df.copy()
    for col in ("total", "mean"):
        if col in out.columns:
            out[col] = out[col].apply(
                lambda x: (math.floor((x / base) + 0.5) * base) if pd.notna(x) else x
            )
    return out
