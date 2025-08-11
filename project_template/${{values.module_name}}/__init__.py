"""ETL Pipeline Module."""

import logging
from typing import Any

from .extract import DataExtractor, extract_from_source
from .load import DataLoader, create_data_summary, save_to_destination
from .transform import DataTransformer, apply_business_rules, normalise_column_names

logger = logging.getLogger(__name__)


class ETLPipeline:
    """Main ETL Pipeline class that orchestrates the entire process."""

    def __init__(self) -> None:
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        self.pipeline_summary = {}

    def run_pipeline(
        self,
        source_path: str,
        output_path: str,
        source_type: str = "csv",
        output_format: str = "csv",
        apply_transforms: bool = True,
        filters: dict[str, Any] | None = None,
    ) -> bool:
        """Run the complete ETL pipeline.

        Args:
            source_path: Path to source data
            output_path: Path for output data
            source_type: Type of source (csv, xlsx, json)
            output_format: Output format (csv, parquet, json)
            apply_transforms: Whether to apply transformations
            filters: Optional filters to apply

        Returns:
            True if pipeline completed successfully, False otherwise
        """
        try:
            logger.info("Starting ETL pipeline")

            # Extract
            logger.info("Phase 1: Extract")
            df = extract_from_source(source_path, source_type)
            self.pipeline_summary["extract"] = {
                "source_path": source_path,
                "rows_extracted": len(df),
                "columns_extracted": len(df.columns),
            }

            # Transform
            logger.info("Phase 2: Transform")
            if apply_transforms:
                # Normalise column names
                df = normalise_column_names(df)

                # Apply business rules
                df = apply_business_rules(df)

                # Apply additional filters if provided
                if filters:
                    df = self.transformer.filter_data(df, filters)

                self.pipeline_summary["transform"] = {
                    "transformations_applied": self.transformer.get_transformation_summary(),
                    "final_rows": len(df),
                    "final_columns": len(df.columns),
                }
            else:
                self.pipeline_summary["transform"] = {
                    "transformations_applied": ["None - transformations skipped"]
                }

            # Load
            logger.info("Phase 3: Load")
            success = save_to_destination(df, output_path, output_format)

            if success:
                # Create data summary
                summary_path = output_path.replace(f".{output_format}", "_summary.json")
                create_data_summary(df, summary_path)

                self.pipeline_summary["load"] = {
                    "output_path": output_path,
                    "summary_path": summary_path,
                    "final_rows": len(df),
                    "status": "success",
                }

                logger.info("ETL pipeline completed successfully")
                return True
            self.pipeline_summary["load"] = {"status": "failed"}
            logger.error("ETL pipeline failed during load phase")
            return False

        except Exception as e:
            logger.exception("ETL pipeline failed")
            self.pipeline_summary["error"] = str(e)
            return False

    def get_pipeline_summary(self) -> dict[str, Any]:
        """Get summary of the pipeline execution.

        Returns:
            Dictionary with pipeline execution summary
        """
        return self.pipeline_summary.copy()


# Convenience function for quick pipeline execution
def run_etl(
    source_path: str,
    output_path: str,
    source_type: str = "csv",
    output_format: str = "csv",
    **kwargs: Any,
) -> bool:
    """Convenience function to run ETL pipeline.

    Args:
        source_path: Path to source data
        output_path: Path for output data
        source_type: Type of source (csv, xlsx, json)
        output_format: Output format (csv, parquet, json)
        **kwargs: Additional arguments for pipeline configuration

    Returns:
        True if pipeline completed successfully, False otherwise
    """
    pipeline = ETLPipeline()
    return pipeline.run_pipeline(source_path, output_path, source_type, output_format, **kwargs)


__all__ = [
    "DataExtractor",
    "DataLoader",
    "DataTransformer",
    "ETLPipeline",
    "apply_business_rules",
    "create_data_summary",
    "extract_from_source",
    "normalise_column_names",
    "run_etl",
    "save_to_destination",
]
