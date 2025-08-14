from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import yaml
import pandas as pd

from .ingestion import load_table
from .estimation import aggregate
from .disclosure import primary_suppression, rounding

@dataclass(frozen=True)
class PipelineConfig:
    input_path: str
    output_dir: str
    group_by: list[str]
    measure: str
    disclosure: dict

    @staticmethod
    def from_yaml(path: str | Path) -> "PipelineConfig":
        data = yaml.safe_load(Path(path).read_text())
        return PipelineConfig(**data)

def run(config: PipelineConfig) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    # Ingest
    raw = load_table(config.input_path)

    # Estimate
    agg = aggregate(raw, config.group_by, config.measure)

    # Disclosure control
    th = int(config.disclosure.get("primary_suppression_threshold", 5))
    base = int(config.disclosure.get("rounding_base", 5))
    protected = primary_suppression(agg, th)
    published = rounding(protected, base)

    # Persist
    out_dir = Path(config.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    agg.to_csv(out_dir / "aggregates.csv", index=False)
    published.to_csv(out_dir / "published.csv", index=False)

    return raw, agg, published
