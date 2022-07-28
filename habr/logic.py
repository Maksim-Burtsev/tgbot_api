from habr.models import Post
from habr.parser import PostDict


def get_unseen_posts(posts: list[PostDict | None]) -> list[PostDict | None]:
    """Return unseen from list of posts. Add them into db (mark as seen)."""

    post_urls = [post["url"] for post in posts]

    db_posts = Post.objects.filter(url__in=post_urls)
    seen_urls = [post.url for post in db_posts]

    unseen_posts = [post for post in posts if post["url"] not in seen_urls]

    new_posts = [Post(url=post["url"]) for post in unseen_posts]
    Post.objects.bulk_create(new_posts)
    return unseen_posts