from typing import TypedDict, Optional
from enum import Enum

import requests
from bs4 import BeautifulSoup


class URL(str, Enum):
    ALL_FLOWS = "https://habr.com/ru/all/"
    WITH_RATING = "https://habr.com/ru/all/top10/"
    TOP_WEEKLY = "https://habr.com/ru/top/weekly/"


class PostDict(TypedDict):
    url: str
    votes: str
    views: str


class ScrapingError(Exception):
    """Status code of response != 200"""

    pass


class ParseDataError(Exception):
    """Failed of getting data from html-block"""

    pass


class Parser:
    """A class which scraping Habr-posts and parse data from them"""


    def _get_html_page(self, url: str) -> str:
        response = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}, proxies={'http':'','https':''}, verify=False)

        if response.status_code == 200:
            return response.text
        else:
            raise ScrapingError("Status code of response != 200")

    def _get_raw_posts(self, page: str) -> list[BeautifulSoup]:

        soup = BeautifulSoup(page, "lxml")

        try:
            posts_block = soup.find_all("div", {"class": "tm-articles-list"})[0]
            raw_posts_list = posts_block.find_all(
                "article", {"class": "tm-articles-list__item"}
            )
        except Exception as e:
            raise ParseDataError(e)

        return raw_posts_list

    def _get_clean_posts(self, raw_posts: list[str]) -> list[PostDict]:

        clean_posts = []
        for post in raw_posts:
            try:
                url = "https://habr.com" + post.find(
                    "a", {"class": "tm-article-snippet__title-link"}
                ).get("href")
                votes = post.find("span", {"data-test-id": "votes-meter-value"}).text
                views = post.find("span", {"class": "tm-icon-counter__value"}).text
            except Exception:
                pass
            else:
                clean_posts.append(PostDict(url=url, votes=votes, views=views))

        return clean_posts

    def _get_url_by_category(self, category: Optional[str]) -> str:

        if category == "top_weekly":
            url = URL.TOP_WEEKLY.value
        elif category == "with_rating":
            url = URL.WITH_RATING.value
        else:
            url = URL.ALL_FLOWS.value

        return url

    def get_posts(self, category: Optional[str] = None) -> list[PostDict]:
        """Return list of posts from first Habr-page with getted category. If category is empty the main page is used"""

        url = self._get_url_by_category(category)

        page = self._get_html_page(url=url)
        raw_posts = self._get_raw_posts(page)
        clean_posts = self._get_clean_posts(raw_posts)

        return clean_posts
