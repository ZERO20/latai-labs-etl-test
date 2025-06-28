"""
Unit tests for the extract module.

This module tests data extraction functionality including API calls,
error handling, and different response scenarios.
"""

import pytest
import requests
from etl.extract import extract_users

TEST_API_URL = "https://jsonplaceholder.typicode.com/users"


class TestExtractUsers:
    """Test cases for extract_users function."""

    def test_extract_users_success(self, requests_mock):
        """Test successful extraction of user data."""
        mock_users = [
            {
                "id": 1,
                "name": "John Doe",
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
                "name": "Jane Smith",
                "email": "jane@example.com",
                "address": {
                    "street": "456 Oak Ave",
                    "suite": "Suite 200",
                    "city": "Los Angeles",
                    "zipcode": "90210",
                },
            },
        ]

        requests_mock.get(TEST_API_URL, json=mock_users)

        result = extract_users(TEST_API_URL)

        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["name"] == "John Doe"
        assert result[1]["id"] == 2
        assert result[1]["name"] == "Jane Smith"

    def test_extract_users_empty_list_response(self, requests_mock):
        """Test handling of empty list response."""
        requests_mock.get(TEST_API_URL, json=[])

        result = extract_users(TEST_API_URL)

        assert result == []
        assert len(result) == 0

    def test_extract_users_timeout(self, requests_mock):
        """Test handling of request timeout."""
        requests_mock.get(TEST_API_URL, exc=requests.exceptions.Timeout)

        with pytest.raises(requests.exceptions.Timeout):
            extract_users(TEST_API_URL)

    def test_extract_users_connection_error(self, requests_mock):
        """Test handling of connection error."""
        requests_mock.get(
            TEST_API_URL, exc=requests.exceptions.ConnectionError
        )

        with pytest.raises(requests.exceptions.ConnectionError):
            extract_users(TEST_API_URL)

    def test_extract_users_generic_request_exception(self, requests_mock):
        """Test handling of generic request exception."""
        requests_mock.get(
            TEST_API_URL, exc=requests.exceptions.RequestException
        )

        with pytest.raises(requests.exceptions.RequestException):
            extract_users(TEST_API_URL)

    def test_extract_users_http_error_404(self, requests_mock):
        """Test handling of HTTP 404 error."""
        requests_mock.get(TEST_API_URL, status_code=404)

        with pytest.raises(requests.exceptions.HTTPError):
            extract_users(TEST_API_URL)

    def test_extract_users_http_error_500(self, requests_mock):
        """Test handling of HTTP 500 error."""
        requests_mock.get(TEST_API_URL, status_code=500)

        with pytest.raises(requests.exceptions.HTTPError):
            extract_users(TEST_API_URL)

    def test_extract_users_invalid_json_response(self, requests_mock):
        """Test handling of invalid JSON response."""
        requests_mock.get(TEST_API_URL, text="Invalid JSON response")

        with pytest.raises(requests.exceptions.JSONDecodeError):
            extract_users(TEST_API_URL)

    def test_extract_users_non_list_response(self, requests_mock):
        """Test handling of response that is not a list."""
        requests_mock.get(
            TEST_API_URL, json={"error": "Invalid response format"}
        )

        with pytest.raises(
            ValueError, match="Expected API response to be a list"
        ):
            extract_users(TEST_API_URL)
