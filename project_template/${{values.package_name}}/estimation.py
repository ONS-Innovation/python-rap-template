from __future__ import annotations
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def aggregate(df: pd.DataFrame, group_by: list[str], measure: str) -> pd.DataFrame:
    """
    Example 'estimation' step: group and compute count, sum, mean for a measure.
    Returns a tidy table with one row per group.
    """
    if not set([*group_by, measure]).issubset(df.columns):
        missing = set([*group_by, measure]) - set(df.columns)
        logger.error(f"Missing columns for aggregation: {missing}")
        raise KeyError(f"Missing columns: {missing}")

    logger.info(f"Aggregating measure '{measure}' by groups {group_by}")
    out = (
        df.groupby(group_by, dropna=False)[measure]
          .agg(n="count", total="sum", mean="mean")
          .reset_index()
    )
    logger.debug(f"Aggregation result:\n{out}")
    # enforce column order
    result = out.loc[:, [*group_by, "n", "total", "mean"]]
    if isinstance(result, pd.Series):
        result = result.to_frame().T
    logger.info(f"Aggregated {len(result)} rows.")
    return result
