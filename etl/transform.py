"""
Handles all data transformations including email validation,
name normalization, address formatting, and duplicate removal.
"""

import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

EMAIL_PATTERN = (
    r"^[a-zA-Z0-9_%+-]+(\.[a-zA-Z0-9_%+-]+)*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)


def validate_email(email: str) -> bool:
    """
    Validate email format using regex.

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if email is valid, False otherwise
    """
    if not email or not isinstance(email, str):
        return False

    email = email.strip()

    return bool(re.match(EMAIL_PATTERN, email))


def normalize_name(name: str) -> str:
    """
    Convert name to uppercase.

    Args:
        name (str): Name to normalize

    Returns:
        str: Name converted to uppercase
    """
    if not name or not isinstance(name, str):
        return ""

    return name.strip().upper()


def create_full_address(address: Dict[str, Any]) -> str:
    """
    Create full address from address components.

    Args:
        address (Dict[str, Any]): Address dictionary with street, suite,
            city, zipcode

    Returns:
        str: Formatted full address
    """
    if not address or not isinstance(address, dict):
        return ""

    components = []

    street = address.get("street", "").strip()
    suite = address.get("suite", "").strip()
    city = address.get("city", "").strip()
    zipcode = address.get("zipcode", "").strip()

    if street:
        components.append(street)
    if suite:
        components.append(suite)
    if city:
        components.append(city)
    if zipcode:
        components.append(zipcode)

    return ", ".join(components)


def remove_duplicates_by_id(
    users: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Remove duplicate users based on ID, keeping the first occurrence.

    Args:
        users (List[Dict[str, Any]]): List of user dictionaries

    Returns:
        List[Dict[str, Any]]: List of users with duplicates removed
    """
    seen_ids = set()
    unique_users = []

    for user in users:
        user_id = user.get("id")
        if user_id is not None and user_id not in seen_ids:
            seen_ids.add(user_id)
            unique_users.append(user)
        elif user_id in seen_ids:
            logger.warning(f"Duplicate ID found and removed: {user_id}")

    return unique_users


def transform_users(users: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Apply all transformations to the users data.

    Args:
        users (List[Dict[str, Any]]): Raw user data from API

    Returns:
        List[Dict[str, Any]]: Transformed user data
    """
    if not users:
        logger.warning("No users data provided for transformation")
        return []

    logger.info(f"Starting transformation of {len(users)} users")

    valid_email_users = []
    for user in users:
        email = user.get("email", "")
        if validate_email(email):
            valid_email_users.append(user)
        else:
            logger.info(f"Removing user with invalid email: {email}")

    logger.info(f"Users with valid emails: {len(valid_email_users)}")

    unique_users = remove_duplicates_by_id(valid_email_users)
    logger.info(f"Users after removing duplicates: {len(unique_users)}")

    transformed_users = []
    for user in unique_users:
        try:
            transformed_user = {
                "id": user.get("id"),
                "name": normalize_name(user.get("name", "")),
                "email": user.get("email", "").strip(),
                "full_address": create_full_address(user.get("address", {})),
            }
            transformed_users.append(transformed_user)
        except Exception as e:
            logger.error(
                f"Error transforming user {user.get('id', 'unknown ID')}: {e}"
            )
            continue

    logger.info(f"Successfully transformed {len(transformed_users)} users")
    return transformed_users
