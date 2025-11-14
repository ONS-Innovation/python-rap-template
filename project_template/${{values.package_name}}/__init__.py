from __future__ import annotations
import argparse
import logging
from .pipeline import PipelineConfig, run

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def app():
    parser = argparse.ArgumentParser(prog="{{ package_name }}", description="RAP sample pipeline")
    parser.add_argument("command", choices=["run"], help="Command to run")
    parser.add_argument("-c", "--config", default="configs/pipeline.yaml", help="Path to config")
    args = parser.parse_args()

    logger.info(f"Starting pipeline with command: {args.command}")
    logger.info(f"Using config file: {args.config}")

    if args.command == "run":
        cfg = PipelineConfig.from_yaml(args.config)
        logger.debug(f"Loaded config: {cfg}")
        _, _, _ = run(cfg)
        logger.info("Pipeline complete.")

__all__ = [
    "PipelineConfig",
    "run",
]