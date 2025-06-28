"""
ETL Package for processing user data from JSONPlaceholder API.

This package provides extraction, transformation, and loading functionality
for user data processing.
"""

__version__ = "1.0.0"
__author__ = "Edgar de la Cruz"

from .extract import extract_users
from .transform import transform_users, validate_email
from .load import load_to_csv

__all__ = ["extract_users", "transform_users", "validate_email", "load_to_csv"]
