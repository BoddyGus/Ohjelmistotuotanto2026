import unittest
from util import validate_reference, UserInputError

class TestValidateReference(unittest.TestCase):
    def test_valid_reference_passes(self):
        validate_reference("book", "key1", "Author", "Title", "2020")

    def test_missing_title_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_reference("book", "key1", "Author", "", "2020")

    def test_missing_author_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_reference("book", "key1", "", "Title", "2020")

    def test_non_numeric_year_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_reference("book", "key1", "Author", "Title", "abc")

    def test_too_long_title_raises_error(self):
        with self.assertRaises(UserInputError):
            validate_reference("book", "key1", "Author", "x" * 201, "2020")