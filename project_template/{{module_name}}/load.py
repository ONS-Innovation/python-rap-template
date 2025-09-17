import json
import logging
from pathlib import Path
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class DataLoader:
    """Class for loading data to various destinations."""

    def __init__(self) -> None:
        self.supported_formats = [".csv", ".xlsx", ".json", ".parquet"]
        self.load_summary: dict[str, Any] = {}

    def load_to_csv(self, df: pd.DataFrame, output_path: str, **kwargs: Any) -> bool:
        """Load DataFrame to CSV file.

        Args:
            df: DataFrame to save
            output_path: Path where to save the CSV file
            **kwargs: Additional arguments for pandas.to_csv

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Loading %d rows to %s", len(df), output_path)

            # Ensure directory exists
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save to CSV
            df.to_csv(output_path, index=False, **kwargs)

            # Update load summary
            self.load_summary[output_path] = {
                "rows": len(df),
                "columns": len(df.columns),
                "format": "csv",
                "status": "success",
            }

            logger.info("Successfully loaded data to %s", output_path)
            return True

        except Exception as e:
            logger.exception("Error loading data to %s", output_path)
            self.load_summary[output_path] = {"status": "failed", "error": str(e)}
            return False

    def load_to_parquet(self, df: pd.DataFrame, output_path: str, **kwargs: Any) -> bool:
        """Load DataFrame to Parquet file.

        Args:
            df: DataFrame to save
            output_path: Path where to save the Parquet file
            **kwargs: Additional arguments for pandas.to_parquet

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Loading %d rows to %s", len(df), output_path)

            # Ensure directory exists
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save to Parquet
            df.to_parquet(output_path, index=False, **kwargs)

            # Update load summary
            self.load_summary[output_path] = {
                "rows": len(df),
                "columns": len(df.columns),
                "format": "parquet",
                "status": "success",
            }

            logger.info("Successfully loaded data to %s", output_path)
            return True

        except Exception as e:
            logger.exception("Error loading data to %s", output_path)
            self.load_summary[output_path] = {"status": "failed", "error": str(e)}
            return False

    def load_to_json(self, df: pd.DataFrame, output_path: str, **kwargs: Any) -> bool:
        """Load DataFrame to JSON file.

        Args:
            df: DataFrame to save
            output_path: Path where to save the JSON file
            **kwargs: Additional arguments for pandas.to_json

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("Loading %d rows to %s", len(df), output_path)

            # Ensure directory exists
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True)

            # Save to JSON
            df.to_json(output_path, orient="records", indent=2, **kwargs)

            # Update load summary
            self.load_summary[output_path] = {
                "rows": len(df),
                "columns": len(df.columns),
                "format": "json",
                "status": "success",
            }

            logger.info("Successfully loaded data to %s", output_path)
            return True

        except Exception as e:
            logger.exception("Error loading data to %s", output_path)
            self.load_summary[output_path] = {"status": "failed", "error": str(e)}
            return False

    def get_load_summary(self) -> dict[str, Any]:
        """Get summary of all load operations.

        Returns:
            dictionary with load operation summaries
        """
        return self.load_summary.copy()

    def validate_output_path(self, output_path: str) -> bool:
        """Validate that the output path is writable.

        Args:
            output_path: Path to validate

        Returns:
            True if path is writable, False otherwise
        """
        try:
            output_dir = Path(output_path).parent
            return output_dir.exists() or output_dir.parent.exists()
        except Exception:
            return False


def save_to_destination(df: pd.DataFrame, output_path: str, format_type: str = "csv") -> bool:
    """Helper function to save DataFrame to specified destination.

    Args:
        df: DataFrame to save
        output_path: Path where to save the file
        format_type: Type of format (csv, parquet, json)

    Returns:
        True if successful, False otherwise
    """
    loader = DataLoader()

    if not loader.validate_output_path(output_path):
        logger.error("Invalid output path: %s", output_path)
        return False

    if format_type.lower() == "csv":
        return loader.load_to_csv(df, output_path)
    if format_type.lower() == "parquet":
        return loader.load_to_parquet(df, output_path)
    if format_type.lower() == "json":
        return loader.load_to_json(df, output_path)
    logger.error("Unsupported format type: %s", format_type)
    return False


def create_data_summary(df: pd.DataFrame, output_path: str) -> bool:
    """Helper function to create a summary of the processed data.

    Args:
        df: DataFrame to summarise
        output_path: Path where to save the summary

    Returns:
        True if successful, False otherwise
    """
    try:
        # Convert datetime columns to string for JSON serialization
        df_for_summary = df.copy()
        for col in df_for_summary.columns:
            if df_for_summary[col].dtype == "datetime64[ns]":
                df_for_summary[col] = df_for_summary[col].astype(str)

        summary = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "column_names": df.columns.tolist(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isna().sum().to_dict(),
            "numeric_summary": (
                df_for_summary.describe().to_dict()
                if len(df_for_summary.select_dtypes(include=["number"]).columns) > 0
                else {}
            ),
        }

        # Ensure directory exists
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w") as f:
            json.dump(summary, f, indent=2)

        logger.info("Data summary saved to %s", output_path)
        return True

    except Exception:
        logger.exception("Error creating data summary")
        return False
