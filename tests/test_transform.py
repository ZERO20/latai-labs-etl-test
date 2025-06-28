"""
Unit tests for the transform module.

This module tests all transformation functions including email validation,
name normalization, address formatting, and duplicate removal.
"""

from etl.transform import (
    validate_email,
    normalize_name,
    create_full_address,
    remove_duplicates_by_id,
    transform_users,
)


class TestEmailValidation:
    """Test cases for email validation function."""

    def test_validate_email_valid_emails(self):
        """Test that valid emails are accepted."""
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "user+tag@example.org",
            "123@test.com",
            "test.email+tag@example.co.uk",
        ]
        for email in valid_emails:
            assert validate_email(email), f"Expected {email} to be valid"

    def test_validate_email_invalid_emails(self):
        """Test that invalid emails are rejected."""
        invalid_emails = [
            "invalid-email",
            "@example.com",
            "test@",
            "test@.com",
            "test..email@example.com",
            "",
            None,
            123,
            "test@example.",
            "test@example",
            "test.example.com",
        ]
        for email in invalid_emails:
            assert not validate_email(email), f"Expected {email} to be invalid"


class TestNameNormalization:
    """Test cases for name normalization function."""

    def test_normalize_name_basic(self):
        """Test basic name normalization to uppercase."""
        assert normalize_name("john doe") == "JOHN DOE"
        assert normalize_name("Jane Smith") == "JANE SMITH"
        assert normalize_name("ALREADY UPPER") == "ALREADY UPPER"

    def test_normalize_name_with_whitespace(self):
        """Test name normalization with whitespace."""
        assert normalize_name("  john doe  ") == "JOHN DOE"
        assert normalize_name("\t\nJane Smith\t\n") == "JANE SMITH"

    def test_normalize_name_edge_cases(self):
        """Test name normalization edge cases.

        Test with empty string, None, whitespace, and number
        """
        assert normalize_name("") == ""
        assert normalize_name(None) == ""
        assert normalize_name("   ") == ""
        assert normalize_name(123) == ""


class TestAddressFormatting:
    """Test cases for address formatting function."""

    def test_create_full_address_complete(self):
        """Test creating full address with all components."""
        address = {
            "street": "123 Main St",
            "suite": "Apt 4B",
            "city": "New York",
            "zipcode": "10001",
        }
        expected = "123 Main St, Apt 4B, New York, 10001"
        assert create_full_address(address) == expected

    def test_create_full_address_partial(self):
        """Test creating full address with missing components."""
        address = {"street": "123 Main St", "city": "New York"}
        expected = "123 Main St, New York"
        assert create_full_address(address) == expected

    def test_create_full_address_empty_components(self):
        """Test creating full address with empty components."""
        address = {
            "street": "123 Main St",
            "suite": "",
            "city": "New York",
            "zipcode": "10001",
        }
        expected = "123 Main St, New York, 10001"
        assert create_full_address(address) == expected

    def test_create_full_address_edge_cases(self):
        """Test address formatting edge cases.

        Test with empty dictionary, None, and empty components
        """
        assert create_full_address({}) == ""
        assert create_full_address(None) == ""
        assert (
            create_full_address(
                {"street": "", "suite": "", "city": "", "zipcode": ""}
            )
            == ""
        )

    def test_create_full_address_with_whitespace(self):
        """Test address formatting with whitespace.

        Test with whitespace in all components
        """
        address = {
            "street": "  123 Main St  ",
            "suite": "  Apt 4B  ",
            "city": "  New York  ",
            "zipcode": "  10001  ",
        }
        expected = "123 Main St, Apt 4B, New York, 10001"
        assert create_full_address(address) == expected


class TestDuplicateRemoval:
    """Test cases for duplicate removal function."""

    def test_remove_duplicates_by_id_no_duplicates(self):
        """Test removing duplicates when there are none.

        Test with no duplicates
        """
        users = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"},
            {"id": 3, "name": "Bob"},
        ]
        result = remove_duplicates_by_id(users)
        assert len(result) == 3
        assert result == users

    def test_remove_duplicates_by_id_with_duplicates(self):
        """Test removing duplicates when they exist.

        Test with duplicates
        """
        users = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"},
            {"id": 1, "name": "John Duplicate"},
            {"id": 3, "name": "Bob"},
        ]
        result = remove_duplicates_by_id(users)
        assert len(result) == 3
        assert result[0]["name"] == "John"
        assert all(
            user["id"] != 1 or user["name"] == "John" for user in result
        )

    def test_remove_duplicates_by_id_edge_cases(self):
        """Test duplicate removal edge cases.

        Test with empty list and None IDs
        """
        assert remove_duplicates_by_id([]) == []

        users = [
            {"id": None, "name": "No ID"},
            {"id": 1, "name": "John"},
            {"id": None, "name": "Another No ID"},
        ]
        result = remove_duplicates_by_id(users)
        assert len(result) == 1


class TestTransformUsers:
    """Test cases for the main transform_users function."""

    def test_transform_users_complete_flow(self):
        """Test complete user transformation flow.

        Test with valid email, invalid email, and duplicate ID
        """
        users = [
            {
                "id": 1,
                "name": "john doe",
                "email": "john@example.com",
                "address": {
                    "street": "123 Main St",
                    "suite": "Apt 1",
                    "city": "New York",
                    "zipcode": "10001",
                },
            },
            {
                "id": 2,
                "name": "jane smith",
                "email": "invalid-email",
                "address": {
                    "street": "456 Oak Ave",
                    "city": "Los Angeles",
                    "zipcode": "90210",
                },
            },
            {
                "id": 3,
                "name": "bob wilson",
                "email": "bob@test.com",
                "address": {
                    "street": "789 Pine St",
                    "city": "Chicago",
                    "zipcode": "60601",
                },
            },
        ]

        result = transform_users(users)

        assert len(result) == 2

        first_user = result[0]
        assert first_user["id"] == 1
        assert first_user["name"] == "JOHN DOE"
        assert first_user["email"] == "john@example.com"
        assert (
            first_user["full_address"] == "123 Main St, Apt 1, New York, 10001"
        )

        second_user = result[1]
        assert second_user["id"] == 3
        assert second_user["name"] == "BOB WILSON"
        assert second_user["email"] == "bob@test.com"
        assert second_user["full_address"] == "789 Pine St, Chicago, 60601"

    def test_transform_users_with_duplicates(self):
        """Test user transformation with duplicate IDs.

        Test with duplicate ID
        """
        users = [
            {
                "id": 1,
                "name": "john doe",
                "email": "john@example.com",
                "address": {"street": "123 Main St", "city": "New York"},
            },
            {
                "id": 1,
                "name": "john duplicate",
                "email": "john.dup@example.com",
                "address": {"street": "456 Oak Ave", "city": "Los Angeles"},
            },
        ]

        result = transform_users(users)

        assert len(result) == 1
        assert result[0]["name"] == "JOHN DOE"

    def test_transform_users_empty_input(self):
        """Test transformation with empty input.

        Test with empty list
        """
        assert len(transform_users([])) == 0

    def test_transform_users_all_invalid_emails(self):
        """Test transformation when all emails are invalid.

        Test with all invalid emails
        """
        users = [
            {
                "id": 1,
                "name": "john doe",
                "email": "invalid-email",
                "address": {"street": "123 Main St"},
            },
            {
                "id": 2,
                "name": "jane smith",
                "email": "also-invalid",
                "address": {"street": "456 Oak Ave"},
            },
        ]

        result = transform_users(users)
        assert len(result) == 0

    def test_transform_users_exception_during_transformation(self, mocker):
        """Test handling of exception during individual user transformation.

        Test with exception during name normalization
        """
        users = [
            {
                "id": 1,
                "name": "john doe",
                "email": "john@example.com",
                "address": {"street": "123 Main St", "city": "New York"},
            },
            {
                "id": 2,
                "name": "jane smith",
                "email": "jane@example.com",
                "address": {"street": "456 Oak Ave", "city": "Los Angeles"},
            },
        ]

        original_normalize_name = normalize_name

        def mock_normalize_name(name):
            if name == "john doe":
                raise ValueError("Mocked error during name normalization")
            return original_normalize_name(name)

        mocker.patch(
            "etl.transform.normalize_name", side_effect=mock_normalize_name
        )

        result = transform_users(users)

        assert len(result) == 1
        assert result[0]["name"] == "JANE SMITH"
        assert result[0]["email"] == "jane@example.com"
