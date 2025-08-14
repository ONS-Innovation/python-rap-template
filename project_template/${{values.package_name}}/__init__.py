from __future__ import annotations
import argparse
from .pipeline import PipelineConfig, run

def app():
    parser = argparse.ArgumentParser(prog="{{ package_name }}", description="RAP sample pipeline")
    parser.add_argument("command", choices=["run"], help="Command to run")
    parser.add_argument("-c", "--config", default="configs/pipeline.yaml", help="Path to config")
    args = parser.parse_args()

    if args.command == "run":
        cfg = PipelineConfig.from_yaml(args.config)
        _, _, _ = run(cfg)
        print("Pipeline complete.")