"""
Unit tests for the load module.

This module tests CSV loading functionality including file creation,
data writing, and validation.
"""

import os
import csv
import tempfile
from etl.load import load_to_csv, validate_csv_file, ensure_output_directory


class TestEnsureOutputDirectory:
    """Test cases for ensure_output_directory function."""

    def test_ensure_output_directory_creates_directory(self):
        """Test that output directory is created when it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "new_dir", "test.csv")
            ensure_output_directory(test_path)
            assert os.path.exists(os.path.dirname(test_path))

    def test_ensure_output_directory_existing_directory(self):
        """Test that function works when directory already exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = os.path.join(temp_dir, "test.csv")
            ensure_output_directory(test_path)
            assert os.path.exists(temp_dir)


class TestLoadToCsv:
    """Test cases for load_to_csv function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.test_users = [
            {
                "id": 1,
                "name": "JOHN DOE",
                "email": "john@example.com",
                "full_address": "123 Main St, New York, 10001",
            },
            {
                "id": 2,
                "name": "JANE SMITH",
                "email": "jane@example.com",
                "full_address": "456 Oak Ave, Los Angeles, 90210",
            },
        ]

    def test_load_to_csv_success(self):
        """Test successful CSV file creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "test_users.csv")

            result = load_to_csv(self.test_users, output_path)

            assert result is True
            assert os.path.exists(output_path)

            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                assert len(rows) == 2
                assert rows[0]["id"] == "1"
                assert rows[0]["name"] == "JOHN DOE"
                assert rows[0]["email"] == "john@example.com"
                assert (
                    rows[0]["full_address"] == "123 Main St, New York, 10001"
                )

    def test_load_to_csv_empty_users(self):
        """Test loading with empty users list."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "empty_users.csv")

            result = load_to_csv([], output_path)

            assert result is False
            assert not os.path.exists(output_path)

    def test_load_to_csv_creates_directory(self):
        """Test that load_to_csv creates output directory if it doesn't
        exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "new_dir", "test_users.csv")

            result = load_to_csv(self.test_users, output_path)

            assert result is True
            assert os.path.exists(output_path)
            assert os.path.exists(os.path.dirname(output_path))

    def test_load_to_csv_missing_fields(self):
        """Test loading users with missing fields."""
        incomplete_users = [
            {
                "id": 1,
                "name": "JOHN DOE",
                # Missing email and full_address
            },
            {
                "email": "jane@example.com",
                "full_address": "456 Oak Ave",
                # Missing id and name
            },
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "incomplete_users.csv")

            result = load_to_csv(incomplete_users, output_path)

            assert result is True

            with open(output_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = list(reader)

                assert len(rows) == 2
                assert rows[0]["id"] == "1"
                assert rows[0]["email"] == ""
                assert rows[1]["name"] == ""

    def test_load_to_csv_io_error(self, mocker):
        """Test handling of IOError during file writing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "io_error_test.csv")

            # Mock open to directly raise IOError
            mocker.patch(
                "builtins.open", side_effect=IOError("Cannot write to file")
            )

            result = load_to_csv(self.test_users, output_path)

            assert result is False

    def test_load_to_csv_generic_exception(self, mocker):
        """Test handling of generic Exception during CSV writing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "exception_test.csv")

            # Mock csv.DictWriter to raise a generic exception (not IOError)
            mocker.patch(
                "csv.DictWriter",
                side_effect=ValueError("Unexpected error during CSV creation"),
            )

            result = load_to_csv(self.test_users, output_path)

            assert result is False


class TestValidateCsvFile:
    """Test cases for validate_csv_file function."""

    def test_validate_csv_file_valid(self):
        """Test validation of a valid CSV file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "valid_users.csv")

            test_users = [
                {
                    "id": 1,
                    "name": "JOHN DOE",
                    "email": "john@example.com",
                    "full_address": "123 Main St, New York",
                }
            ]

            load_to_csv(test_users, output_path)

            result = validate_csv_file(output_path)
            assert result is True

    def test_validate_csv_file_nonexistent(self):
        """Test validation of a non-existent file."""
        result = validate_csv_file("non_existent_file.csv")
        assert result is False

    def test_validate_csv_file_wrong_headers(self):
        """Test validation of CSV with wrong headers."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "wrong_headers.csv")

            # Create CSV with wrong headers
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["wrong", "headers", "here"])
                writer.writerow(["1", "John", "test@example.com"])

            result = validate_csv_file(output_path)
            assert result is False

    def test_validate_csv_file_empty_file(self):
        """Test validation of an empty CSV file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "empty.csv")

            # Create empty file
            with open(output_path, "w", encoding="utf-8"):
                pass

            result = validate_csv_file(output_path)
            assert result is False

    def test_validate_csv_file_correct_headers_no_data(self):
        """Test validation of CSV with correct headers but no data rows."""
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, "headers_only.csv")

            # Create CSV with only headers
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["id", "name", "email", "full_address"])

            result = validate_csv_file(output_path)
            assert result is True
