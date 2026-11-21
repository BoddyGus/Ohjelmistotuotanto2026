import unittest

from app import app
from db_helper import setup_db
from repositories.reference_repository import add_reference, get_reference, get_references


class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()

    def test_existing_reference_can_be_retrieved(self):
        with app.app_context():
            add_reference(
                "key1",
                "book",
                "Author",
                "Title",
                2020,
                "Publisher",
            )

            references = get_references()
            reference = get_reference(references[0].id)

        self.assertIsNotNone(reference)
        self.assertEqual(reference.citation_key, "key1")

    def test_unknown_reference_returns_none(self):
        with app.app_context():
            reference = get_reference(999)

        self.assertIsNone(reference)