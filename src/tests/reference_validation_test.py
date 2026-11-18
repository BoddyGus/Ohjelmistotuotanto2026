import unittest

from reference_validation import ReferenceValidationError, validate_reference


class TestReferenceValidation(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
