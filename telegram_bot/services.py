import os
import calendar
import datetime
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


def delete_notes(query: str) -> bool:
    """Delete notes with query. First GET pk of notes with name and category, which contains query. Second is DELETE them"""
    notes_with_name = _get_notes_pk(name=query)
    notes_with_category = _get_notes_pk(category=query)

    notes_for_delete = set(notes_with_name + notes_with_category)

    if notes_for_delete:
        for pk in notes_for_delete:
            requests.delete(f"{URL}/notes/{pk}/")
        return True
    return False


def _get_notes_pk(
    name: str | None = None, category: str | None = None
) -> list[int | None]:
    """GET notes with name | category and return list of their pk"""
    if not name and not category: return []

    if name:
        response = requests.get(f"{URL}/notes/?name={name.title()}")

    elif category:
        response = requests.get(f"{URL}/notes/?category={category.lower()}")

    if response.status_code == 200 and response.json():
        pk_list = [note["pk"] for note in response.json()]
        return pk_list

    return []


def create_note(
    name: str, category: str | None = None, description: str | None = None
) -> bool:
    """Create note with current datetime"""
    date_today = str(datetime.datetime.now())
    data = {
        "name": name,
        "date": date_today,
        "category": category,
        "description": description,
    }
    response = requests.post(f"{URL}/notes/", json=data)

    return response.status_code == 201


def get_monthly_costs(month: int, year: int) -> str:
    """Get total costs of this year and month"""
    response = requests.get(f"{URL}/get_monthly_costs/?month={month}&year={year}")
    if response.status_code == 200:
        data = response.json()
        if data:
            return f"Total: {response.json()['total']}"
    return "invalid month or year"


def remove_purchase(name: str) -> bool:
    """Remove purhase by name - get id from GET request and if this purchase exists make DELETE request"""
    response = requests.get(f"{URL}/purchases/?name={name.title()}")
    if response.status_code == 200:
        data = response.json()
        if data:
            purchase_id = data[0]["id"]
            response = requests.delete(f"{URL}/purchases/{purchase_id}/")
            return True
    return False


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
    pk = 324235235235235
    response = requests.delete(f"{URL}/notes/{pk}/")
