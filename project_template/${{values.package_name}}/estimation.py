from __future__ import annotations
import pandas as pd

def aggregate(df: pd.DataFrame, group_by: list[str], measure: str) -> pd.DataFrame:
    """
    Example 'estimation' step: group and compute count, sum, mean for a measure.
    Returns a tidy table with one row per group.
    """
    if not set([*group_by, measure]).issubset(df.columns):
        missing = set([*group_by, measure]) - set(df.columns)
        raise KeyError(f"Missing columns: {missing}")

    out = (
        df.groupby(group_by, dropna=False)[measure]
          .agg(n="count", total="sum", mean="mean")
          .reset_index()
    )
    # enforce column order
    result = out.loc[:, [*group_by, "n", "total", "mean"]]
    if isinstance(result, pd.Series):
        result = result.to_frame().T
    return result
