import os
import calendar
from datetime import date
from typing import NamedTuple

import requests
from dotenv import load_dotenv

from telebot import TeleBot
from telebot.types import Message


load_dotenv()
URL = os.getenv("URL")


class MonthStartEndDates(NamedTuple):
    start_date: str
    end_date: str


def send_purchases(bot: TeleBot, message: Message, purchases_list: list[str]) -> None:
    """Send list of purchases"""
    for purchase in purchases_list:
        bot.send_message(message.chat.id, purchase)


def get_current_month_dates() -> MonthStartEndDates:
    """Return first and last day (in date format) of current month"""
    today_date = date.today()
    year, month = today_date.year, today_date.month

    last_day = calendar.monthrange(year, month)[-1]

    return MonthStartEndDates(f"{year}-{month}-01", f"{year}-{month}-{last_day}")


def send_posts(bot: TeleBot, message: Message, posts: list[str]) -> None:
    """Send list of posts"""
    if posts:
        for post in posts:
            bot.send_message(message.chat.id, post)


def get_habr_posts(category: str | None = None) -> list[str | None]:
    """Parse habr posts with this category and return them formatted"""
    response = requests.get(f"{URL}/habr/get_posts/?category={category}")
    if response.status_code == 200:
        data = response.json()
        if data:
            posts_list = [
                f"views:{post['views']}\nvotes:{post['votes']}\n\n{post['url']}"
                for post in data
            ]
            return posts_list
    return []


def get_purchases_report(from_date: str = "", to_date: str = "") -> list[str]:
    """Parse purchases list for this period, count total and format every purchase in str"""
    response = requests.get(
        f"{URL}/get_purchases/?from_date={from_date}&to_date={to_date}"
    )
    if response.status_code == 200:
        purchases_list = []
        total_cost = 0

        for purchase in response.json():

            name = f"{purchase['name']}"
            total = purchase["total"]
            total_cost += total
            count = purchase["count"]

            if count > 1:
                purchases_list.append(f"{name} {total}р. ({purchase['count']})\n")
            else:
                purchases_list.append(f"{name} {total}р.\n")

        purchases_list.append(f"Total: {total_cost}р.")
        return purchases_list


if __name__ == "__main__":
    print(get_current_month_dates())
