from typing import TypedDict
from enum import Enum

import requests
from bs4 import BeautifulSoup
import fake_useragent


class URL(Enum):
    ALL_FLOWS = "https://habr.com/ru/all/"
    WITH_RATING = "https://habr.com/ru/all/top10/"
    TOP_WEEKLY = "https://habr.com/ru/top/weekly/"


class PostDict(TypedDict):
    url: str
    votes: str
    views: str


class Parser:
    def __init__(self) -> None:

        self.headers = {"user-agent": fake_useragent.UserAgent().random}

    def _get_html_page(self, url: str) -> str:

        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Parsing error")

    def _get_raw_posts_from_page(self, page) -> list[str]:

        soup = BeautifulSoup(page, "lxml")

        posts_block = soup.find_all("div", {"class": "tm-articles-list"})[0]
        raw_posts_list = posts_block.find_all(
            "article", {"class": "tm-articles-list__item"}
        )

        return raw_posts_list

    def _get_clean_posts(self, raw_posts) -> list[PostDict]:

        clean_posts = []
        #TODO add try/except block
        for post in raw_posts:
            url = "https://habr.com" + post.find(
                "a", {"class": "tm-article-snippet__title-link"}
            ).get("href")
            votes = post.find("span", {"data-test-id": "votes-meter-value"}).text
            views = post.find("span", {"class": "tm-icon-counter__value"}).text

            clean_posts.append(PostDict(url=url, votes=votes, views=views))

        return clean_posts

    def _get_url_by_category(self, category: str | None) -> str:

        if category == "top_weekly":
            url = URL.TOP_WEEKLY.value
        elif category == "with_rating":
            url = URL.WITH_RATING.value
        else:
            url = URL.ALL_FLOWS.value

        return url

    def get_posts(self, category: str | None = None) -> list[PostDict]:

        url = self._get_url_by_category(category)

        page = self._get_html_page(url=url)
        raw_posts = self._get_raw_posts_from_page(page)
        clean_posts = self._get_clean_posts(raw_posts)

        return clean_posts
