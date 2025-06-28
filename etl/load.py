"""
Handles saving transformed data to CSV files.
"""

import csv
import os
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def ensure_output_directory(output_path: str) -> None:
    """
    Ensure the output directory exists, create if it doesn't.

    Args:
        output_path (str): Path to the output file
    """
    directory = os.path.dirname(output_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        logger.info(f"Created output directory: {directory}")


def load_to_csv(users: List[Dict[str, Any]], output_path: str) -> bool:
    """
    Save transformed user data to a CSV file.

    Args:
        users (List[Dict[str, Any]]): Transformed user data
        output_path (str): Path to save the CSV file

    Returns:
        bool: True if successful, False otherwise
    """
    if not users:
        logger.warning("No users data provided for loading")
        return False

    try:
        ensure_output_directory(output_path)

        fieldnames = ["id", "name", "email", "full_address"]

        logger.info(f"Saving {len(users)} users to {output_path}")

        with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user in users:
                row = {
                    "id": user.get("id", ""),
                    "name": user.get("name", ""),
                    "email": user.get("email", ""),
                    "full_address": user.get("full_address", ""),
                }
                writer.writerow(row)

        logger.info(f"Successfully saved data to {output_path}")
        return True

    except IOError as e:
        logger.error(f"Failed to write to file {output_path}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while saving to CSV: {e}")
        return False


def validate_csv_file(file_path: str) -> bool:
    """
    Validate that the CSV file was created correctly.

    Args:
        file_path (str): Path to the CSV file to validate

    Returns:
        bool: True if file exists and is valid, False otherwise
    """
    try:
        if not os.path.exists(file_path):
            logger.error(f"CSV file does not exist: {file_path}")
            return False

        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            expected_fields = {"id", "name", "email", "full_address"}

            if set(reader.fieldnames) != expected_fields:
                logger.error(
                    f"CSV has incorrect fields. Expected: {expected_fields}, "
                    f"Got: {set(reader.fieldnames)}"
                )
                return False

            row_count = sum(1 for row in reader)
            logger.info(
                f"CSV validation successful. File has {row_count} data rows"
            )
            return True

    except Exception as e:
        logger.error(f"Error validating CSV file: {e}")
        return False
