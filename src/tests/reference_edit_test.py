import unittest

from app import app
from db_helper import setup_db
from repositories.reference_repository import add_reference, get_references


class TestReferenceEdit(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        with app.app_context():
            setup_db()
            add_reference("original", "book", "Author", "Title", 2020, "Publisher")
            self.reference_id = get_references()[0].id
        self.client = app.test_client()

    def test_edit_form_is_prefilled_and_updates_all_fields(self):
        response = self.client.get(f"/references/{self.reference_id}/edit")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'value="original"', response.data)
        self.assertIn(b'value="Publisher"', response.data)

        response = self.client.post(
            f"/references/{self.reference_id}/edit",
            data={
                "citation_key": "updated-key",
                "type": "article",
                "author": "Updated Author",
                "title": "Updated Title",
                "year": "2021",
                "publication": "Updated Journal",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, f"/references/{self.reference_id}")
        details = self.client.get(response.location)
        self.assertIn(b"updated-key", details.data)
        self.assertIn(b"Updated Author", details.data)
        self.assertIn(b"Updated Title", details.data)
        self.assertIn(b"Updated Journal", details.data)

    def test_edit_rejects_duplicate_citation_key(self):
        with app.app_context():
            add_reference("already-used", "book", "Author", "Title", 2020, None)

        response = self.client.post(
            f"/references/{self.reference_id}/edit",
            data={
                "citation_key": "already-used",
                "type": "book",
                "author": "Author",
                "title": "Title",
                "year": "2020",
                "publication": "",
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"The citation key is already in use.", response.data)

    def test_unknown_reference_cannot_be_edited(self):
        response = self.client.get("/references/999999/edit")

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Reference not found", response.data)


if __name__ == "__main__":
    unittest.main()
