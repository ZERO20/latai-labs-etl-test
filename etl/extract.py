"""
Handles the extraction of user data from the JSONPlaceholder API.
"""

import logging
import requests
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


def extract_users(url: str) -> List[Dict[str, Any]]:
    """
    Extract user data from the JSONPlaceholder API.

    Args:
        url (str): API endpoint URL to fetch user data from

    Returns:
        List[Dict[str, Any]]: List of user dictionaries

    Raises:
        requests.RequestException: If the API request fails
        ValueError: If the response is not valid JSON
    """
    try:
        logger.info(f"Fetching user data from {url}")

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        users_data = response.json()

        if not isinstance(users_data, list):
            raise ValueError("Expected API response to be a list")

        logger.info(f"Successfully extracted {len(users_data)} users")
        return users_data

    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        raise
    except requests.exceptions.ConnectionError:
        logger.error("Connection error occurred")
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error occurred: {e}")
        raise
    except requests.exceptions.JSONDecodeError as e:
        logger.error(f"Invalid JSON response: {e}")
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid response format: {e}")
        raise
