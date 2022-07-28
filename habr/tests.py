from django.test import TestCase

from habr.logic import get_unseen_posts, PostDict
from habr.models import Post


class HabrTestCase(TestCase):
    def test_get_posts(self):

        response = self.client.get("/habr/get_posts/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 20)

    def test_get_unseen_posts(self):
        posts = [
            PostDict(url=f"https://habr.com/article12421{i}", votes=i, views=i)
            for i in range(10)
        ]

        for i in range(1, 10):
            Post.objects.create(url=f"https://habr.com/article12421{i}")

        unseen_posts = get_unseen_posts(posts)

        self.assertEqual(len(unseen_posts), 1)
        self.assertEqual(
            unseen_posts,
            [{"url": "https://habr.com/article124210", "votes": 0, "views": 0}],
        )
