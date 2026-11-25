from datetime import date
import unittest
from types import SimpleNamespace

from reference_validation import (
    ReferenceValidationError,
    is_duplicate_citation_key,
    validate_reference,
)


class TestReferenceValidation(unittest.TestCase):
    def test_duplicate_citation_key_integrity_error_is_detected(self):
        error = SimpleNamespace(
            orig=Exception(
                "UNIQUE constraint failed: bibliographic_references.citation_key"
            )
        )

        self.assertTrue(is_duplicate_citation_key(error))

    def test_other_integrity_error_is_not_a_duplicate_citation_key(self):
        error = SimpleNamespace(
            orig=Exception(
                "NOT NULL constraint failed: bibliographic_references.title"
            )
        )

        self.assertFalse(is_duplicate_citation_key(error))

    def test_missing_required_field_raises_error(self):
        with self.assertRaisesRegex(
            ReferenceValidationError, "Citation key"
        ):
            validate_reference(
                {
                    "citation_key": " ",
                    "type": "book",
                    "author": "Ada Lovelace",
                    "title": "Notes",
                    "year": "1843",
                }
            )

    def test_valid_data_is_normalized_and_publication_is_optional(self):
        reference = validate_reference(
            {
                "citation_key": " lovelace1843 ",
                "type": " book ",
                "author": " Ada Lovelace ",
                "title": " Notes ",
                "year": "1843",
            }
        )

        self.assertEqual(
            reference,
            {
                "citation_key": "lovelace1843",
                "reference_type": "book",
                "author": "Ada Lovelace",
                "title": "Notes",
                "year": 1843,
                "publication": None,
            },
        )

    def test_non_numeric_year_raises_error(self):
        with self.assertRaisesRegex(ReferenceValidationError, "Year must be a number"):
            validate_reference(
                {
                    "citation_key": "lovelace1843",
                    "type": "book",
                    "author": "Ada Lovelace",
                    "title": "Notes",
                    "year": "not a year",
                }
            )

    def test_negative_year_raises_error(self):
        with self.assertRaisesRegex(ReferenceValidationError, "Year must be positive"):
            validate_reference(
                {
                    "citation_key": "lovelace1843",
                    "type": "book",
                    "author": "Ada Lovelace",
                    "title": "Notes",
                    "year": "-1843",
                }
            )

    def test_zero_year_raises_error(self):
        with self.assertRaisesRegex(ReferenceValidationError, "Year must be positive"):
            validate_reference(
                {
                    "citation_key": "lovelace1843",
                    "type": "book",
                    "author": "Ada Lovelace",
                    "title": "Notes",
                    "year": "0",
                }
            )

    def test_future_year_raises_error(self):
        future_year = date.today().year + 1
        with self.assertRaisesRegex(ReferenceValidationError, "Year cannot be in the future"):
            validate_reference(
                {
                    "citation_key": "future",
                    "type": "book",
                    "author": "Ada Lovelace",
                    "title": "Notes",
                    "year": str(future_year),
                }
            )

    def test_current_year_is_valid(self):
        reference = validate_reference(
            {
                "citation_key": "current",
                "type": "book",
                "author": "Ada Lovelace",
                "title": "Notes",
                "year": str(date.today().year),
            }
        )

        self.assertEqual(reference["year"], date.today().year)


if __name__ == "__main__":
    unittest.main()
