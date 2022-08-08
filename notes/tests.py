import json

from django.test import TestCase

from notes.models import Note


class NoteViewTest(TestCase):
    def setUp(self) -> None:
        self.note1 = Note.objects.create(
            name="test note",
        )
        Note.objects.create(
            name="test note two", description="something text", category="Test cat"
        )
        return super().setUp()

    def test_create_note(self):
        data = {"name": "poST 1", "category": "FROM REQUEST"}
        response = self.client.post(
            "/notes/", data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Post 1")
        self.assertEqual(response.json()["category"], "from request")

    def test_create_without_category(self):
        data = {"name": "post 2"}
        response = self.client.post(
            "/notes/", data=json.dumps(data), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["name"], "Post 2")

    def test_delete_note(self):
        response = self.client.delete(f"/notes/{self.note1.id}/")

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Note.DoesNotExist):
            self.note1.refresh_from_db()

    def test_delete_note_404(self):
        wrong_id = 351325412
        response = self.client.delete(f"/notes/{wrong_id}/")

        self.assertEqual(response.status_code, 404)

    def test_get_notes(self):
        response = self.client.get("/notes/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_notes_with_category_filter(self):
        response = self.client.get("/notes/?category=test%20cat")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["category"], "test cat")
        self.assertEqual(response.json()[0]["name"], "Test note two")

    def test_get_notes_with_name_filter(self):
        response = self.client.get("/notes/?name=not")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_get_notes_empty_category(self):
        response = self.client.get("/notes/?category=empty_cat")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_get_notes_emty_names(self):
        response = self.client.get("/notes/?name=empty_name")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])
