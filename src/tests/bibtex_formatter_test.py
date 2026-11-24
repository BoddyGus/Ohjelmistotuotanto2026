import unittest

from entities.reference import Reference
from repositories.bibtex_formatter import (
    format_inproceeding_reference,
    format_article_reference,
    format_book_reference,
)

class TestBibtexFromatter(unittest.TestCase):
    def test_formats_inproceedings_reference(self):
        reference = Reference(
            1, "key1", "inproceedings", "Author", "Paper", 2022, "Conference"
        )
        result = format_inproceeding_reference(reference)

        self.assertIn("@inproceedings{key1,", result)
        self.assertIn("booktitle = {Conference}", result)

    def test_fromats_article_reference(self):
        reference = Reference(
            1, "key2", "article", "Author", "Article", 2021, "Journal"
        )

        result = format_article_reference(reference)

        self.assertIn("@article{key2,",result)
        self.assertIn("journal = {Journal}", result)

    def test_formats_book_reference(self):
        reference = Reference(
            1, "key3", "book", "Author", "Title", 2020, "Publisher"
        )

        result = format_book_reference(reference)

        self.assertIn("@book{key3,", result)
        self.assertIn("author = {Author}", result)
        self.assertIn("title = {Title}", result)
        self.assertIn("year = {2020}", result)
        self.assertIn("publisher = {Publisher}", result)

    def test_empty_publicationd_fields_omitted(self):
        cases = [
            (format_inproceeding_reference, "inproceedings", "booktitle"),
            (format_article_reference, "article", "journal"),
            (format_book_reference, "book", "publisher"),
        ]

        for formatter, reference_type, field in cases:
            for publication in (None, "", " "):
                with self.subTest(
                    reference_type=reference_type,
                    publication=publication,
                ):
                    reference = Reference(
                        4, "key4", reference_type,
                        "Author", "Title", 2020, publication,
                    )
                    result = formatter(reference)

                    self.assertIn("year = {2020}", result)
                    self.assertNotIn(f"{field} =", result)
