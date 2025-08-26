import logging
from typing import Any

import pandas as pd

logger = logging.getLogger(__name__)


class DataTransformer:
    """Class for transforming and cleaning data."""

    def __init__(self) -> None:
        self.transformation_log: list[str] = []

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean the data by removing duplicates and handling missing values.

        Args:
            df: Input DataFrame

        Returns:
            Cleaned DataFrame
        """
        logger.info("Starting data cleaning process")

        # Remove duplicates
        initial_rows = len(df)
        df_cleaned = df.drop_duplicates()
        duplicates_removed = initial_rows - len(df_cleaned)

        if duplicates_removed > 0:
            logger.info("Removed %d duplicate rows", duplicates_removed)
            self.transformation_log.append(f"Removed {duplicates_removed} duplicates")

        # Handle missing values - fill numeric columns with median, categorical with mode
        for column in df_cleaned.columns:
            if df_cleaned[column].isna().any():
                if df_cleaned[column].dtype in ["int64", "float64"]:
                    df_cleaned[column] = df_cleaned[column].fillna(df_cleaned[column].median())
                    logger.info("Filled missing values in %s with median", column)
                else:
                    mode_value = df_cleaned[column].mode()
                    if not mode_value.empty:
                        df_cleaned[column] = df_cleaned[column].fillna(mode_value[0])
                        logger.info("Filled missing values in %s with mode", column)

        return df_cleaned

    def add_calculated_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add calculated columns based on existing data.

        Args:
            df: Input DataFrame

        Returns:
            DataFrame with additional calculated columns
        """
        df_transformed = df.copy()

        # Example transformations - adjust based on your data structure
        if "quantity" in df.columns and "price" in df.columns:
            df_transformed["total_value"] = df_transformed["quantity"] * df_transformed["price"]
            logger.info("Added total_value column")
            self.transformation_log.append("Added total_value column")

        if "date" in df.columns:
            df_transformed["date"] = pd.to_datetime(df_transformed["date"])
            df_transformed["year"] = df_transformed["date"].dt.year
            df_transformed["month"] = df_transformed["date"].dt.month
            df_transformed["day_of_week"] = df_transformed["date"].dt.day_name()
            logger.info("Added date-based columns")
            self.transformation_log.append("Added date-based columns")

        return df_transformed

    def filter_data(self, df: pd.DataFrame, filters: dict[str, Any]) -> pd.DataFrame:
        """Filter data based on given criteria.

        Args:
            df: Input DataFrame
            filters: Dictionary of column names and filter criteria

        Returns:
            Filtered DataFrame
        """
        df_filtered = df.copy()

        for column, criteria in filters.items():
            if column in df_filtered.columns:
                if isinstance(criteria, dict):
                    if "min" in criteria:
                        df_filtered = df_filtered[df_filtered[column] >= criteria["min"]]
                    if "max" in criteria:
                        df_filtered = df_filtered[df_filtered[column] <= criteria["max"]]
                elif isinstance(criteria, list):
                    df_filtered = df_filtered[df_filtered[column].isin(criteria)]
                else:
                    df_filtered = df_filtered[df_filtered[column] == criteria]

                logger.info("Applied filter on %s: %s", column, criteria)
                self.transformation_log.append(f"Applied filter on {column}")

        return df_filtered

    def get_transformation_summary(self) -> list[str]:
        """Get summary of all transformations applied.

        Returns:
            List of transformation descriptions
        """
        return self.transformation_log.copy()


def apply_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """Helper function to apply business-specific transformation rules.

    Args:
        df: Input DataFrame

    Returns:
        Transformed DataFrame
    """
    transformer = DataTransformer()

    # Clean the data
    df_cleaned = transformer.clean_data(df)

    # Add calculated columns
    df_enhanced = transformer.add_calculated_columns(df_cleaned)

    # Apply any business-specific filters
    # Example: filter out negative quantities
    if "quantity" in df_enhanced.columns:
        df_filtered = transformer.filter_data(df_enhanced, {"quantity": {"min": 0}})
    else:
        df_filtered = df_enhanced

    logger.info("Business rules applied successfully")
    return df_filtered


def normalise_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Helper function to normalise column names.

    Args:
        df: Input DataFrame

    Returns:
        DataFrame with normalised column names
    """
    df_normalised = df.copy()
    df_normalised.columns = (
        df_normalised.columns.str.lower().str.replace(" ", "_").str.replace("-", "_")
    )
    logger.info("Column names normalised")
    return df_normalised
