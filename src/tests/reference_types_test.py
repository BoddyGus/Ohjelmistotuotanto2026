import unittest
from reference_types import (
    REFERENCE_TYPES,
    get_reference_type,
    get_reference_types,
)


class TestReferenceTypes(unittest.TestCase):
    def test_supported_types_are_book_article_and_inproceedings(self):
        names = {t.name for t in get_reference_types()}
        self.assertEqual(names, {"book", "article", "inproceedings"})

    def test_type_can_be_found_by_name(self):
        for name in ("book", "article", "inproceedings"):
            self.assertEqual(get_reference_type(name).name, name)

    def test_unknown_type_returns_none(self):
        self.assertIsNone(get_reference_type("thesis"))
        self.assertIsNone(get_reference_type(""))

    def test_publication_meaning_depends_on_type(self):
        self.assertEqual(get_reference_type("book").bibtex_field, "publisher")
        self.assertEqual(get_reference_type("article").bibtex_field, "journal")
        self.assertEqual(
            get_reference_type("inproceedings").bibtex_field, "booktitle"
        )

    def test_every_type_has_user_facing_labels(self):
        for reference_type in REFERENCE_TYPES.values():
            self.assertTrue(reference_type.label)
            self.assertTrue(reference_type.publication_label)