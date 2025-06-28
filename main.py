"""
ETL script for processing user data from JSONPlaceholder API.

This script orchestrates the complete ETL process:
1. Extract users from the JSONPlaceholder API
2. Transform the data (validate emails, normalize names, create full addresses,
   remove duplicates)
3. Load the processed data to a CSV file
"""

import logging
import sys
from etl.extract import extract_users
from etl.transform import transform_users
from etl.load import load_to_csv, validate_csv_file

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("etl_process.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

# Configuration
API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_PATH = "output/users_cleaned.csv"


def main():
    """
    Main function to execute the complete ETL process.
    """
    try:
        logger.info("=" * 50)
        logger.info("Starting ETL Process")
        logger.info("=" * 50)

        logger.info("Step 1: Extracting user data from API")
        raw_users = extract_users(API_URL)

        if not raw_users:
            logger.error("No data extracted from API. Exiting.")
            sys.exit(1)

        logger.info("Step 2: Transforming users data")
        transformed_users = transform_users(raw_users)

        if not transformed_users:
            logger.warning("No users remaining after transformation")

        logger.info("Step 3: Loading data to CSV")
        success = load_to_csv(transformed_users, OUTPUT_PATH)

        if not success:
            logger.error("Failed to save data to CSV. Exiting.")
            sys.exit(1)

        logger.info("Step 4: Validating output file")
        if validate_csv_file(OUTPUT_PATH):
            logger.info("ETL process completed successfully!")
            logger.info(f"Processed {len(transformed_users)} users")
            logger.info(f"Output saved to: {OUTPUT_PATH}")
        else:
            logger.error("Output file validation failed")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("ETL process interrupted by user")
    except Exception as e:
        logger.error(f"ETL process failed with error: {e}")
        sys.exit(1)
    finally:
        logger.info("=" * 50)
        logger.info("ETL Process Ended")
        logger.info("=" * 50)


if __name__ == "__main__":
    main()
