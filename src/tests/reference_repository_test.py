import unittest

from app import app
from db_helper import setup_db
from repositories.reference_repository import (
    add_reference,
    get_reference,
    get_references,
    update_reference,
    delete_reference
)


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

    def test_existing_reference_can_be_updated(self):
        with app.app_context():
            add_reference("key1", "book", "Author", "Title", 2020, "Publisher")
            reference_id = get_references()[0].id

            update_reference(
                reference_id,
                "new-key",
                "article",
                "New Author",
                "New Title",
                2021,
                "New Journal",
            )
            reference = get_reference(reference_id)

        self.assertEqual(reference.citation_key, "new-key")
        self.assertEqual(reference.type, "article")
        self.assertEqual(reference.author, "New Author")
        self.assertEqual(reference.title, "New Title")
        self.assertEqual(reference.year, 2021)
        self.assertEqual(reference.publication, "New Journal")

    def test_deleted_reference_is_removed(self):
        with app.app_context():
            add_reference("key1", "book", "Author", "Title", 2020, "Publisher")
            reference_id = get_references()[0].id

            delete_reference(reference_id)
            reference = get_reference(reference_id)

        self.assertIsNone(reference)
    
    def test_deleting_one_reference_keeps_the_others(self):
        with app.app_context():
            add_reference("key1", "book", "Author1", "Title1", 2020, "Publisher1")
            add_reference("key2", "article", "Author2", "Title2", 2021, "Publisher2")
            reference_id_to_delete = get_references()[0].id

            delete_reference(reference_id_to_delete)
            remaining_references = get_references()

        self.assertEqual(len(remaining_references), 1)
        self.assertEqual(remaining_references[0].citation_key, "key2")

    def test_deleting_non_existent_reference_does_nothing(self):
        with app.app_context():
            add_reference("key1", "book", "Author1", "Title1", 2020, "Publisher1")
            initial_references = get_references()
            delete_reference(999)
            remaining_references = get_references()

        self.assertEqual(len(remaining_references), len(initial_references))