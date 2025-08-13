
import logging

# Import RAP modules
from .disclosure import primary_suppression, rounding
from .estimation import aggregate
from .ingestion import load_table

logger = logging.getLogger(__name__)


def run_rap_example():
    """
    Example script to demonstrate RAP workflow using example_data.csv.
    Loads data, aggregates statistics, applies disclosure control, and prints results.
    """
    import os
    import logging
    logging.basicConfig(level=logging.INFO)
    # Path to example data
    data_path = os.path.join(os.path.dirname(__file__), '..', 'example_data.csv')
    data_path = os.path.abspath(data_path)
    logging.info(f"Loading data from: {data_path}")
    # Load data
    df = load_table(data_path)
    logging.info("Loaded data:")
    logging.info(df.head())
    # Estimate statistics (aggregate)
    list_of_groups = ['region', 'category']  # Example group columns from example_data.csv
    results = aggregate(df, group_by=list_of_groups, measure='quantity')  # Aggregate by quantity
    logging.info("Estimation results:")
    logging.info(results)
    # Apply disclosure control (primary_suppression + rounding)
    threshold = 2  # Example: suppress groups with less than 2 items
    suppressed = primary_suppression(results, threshold)
    base = 5  # Example: round to nearest 5
    rounded = rounding(suppressed, base)
    logging.info("Disclosure controlled results:")
    logging.info(rounded)
