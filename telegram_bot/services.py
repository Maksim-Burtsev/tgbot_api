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


def create_purchases(raw_purchases: list[str]) -> bool:
    """Create json with purchases and make POST request"""
    today_date = str(date.today())
    purchases_list = []

    for i in range(0, len(raw_purchases), 2):
        purchases_list.append(
            {"name": raw_purchases[i], "cost": raw_purchases[i + 1], "date": today_date}
        )
    response = requests.post(f"{URL}/purchases/", json=purchases_list)
    return response.status_code == 201


def get_notes(query: str) -> list[str | None]:
    """Return list of formatted notes on this query"""
    raw_notes = _get_notes(category=query)
    if not raw_notes:
        raw_notes = _get_notes(name=query)

    notes_list = []
    for note in raw_notes:
        note = _format_note(note)
        notes_list.append(note)

    return notes_list


def _format_note(note: dict) -> str:
    """Format note dict into a str"""
    res = note["name"]

    if note["description"]:
        res += f"\n{note['description']}"

    if note["category"]:
        res += f"\n\n{note['category']}"

    if note["date"]:
        res += f", {note['date'][:10]}"

    return res


def delete_notes(query: str) -> bool:
    """Delete notes with query. First GET pk of notes with name and category, which contains query. Second is DELETE them"""
    with_name = [note["pk"] for note in _get_notes(name=query) if note]
    with_category = [note["pk"] for note in _get_notes(category=query) if note]

    pk_notes_for_delete = set(with_name + with_category)

    if pk_notes_for_delete:
        for pk in pk_notes_for_delete:
            requests.delete(f"{URL}/notes/{pk}/")
        return True
    return False


def _get_notes(
    name: str | None = None, category: str | None = None
) -> list[int | None]:
    """GET notes with name | category"""
    if name:
        response = requests.get(f"{URL}/notes/?name={name.title()}")
    elif category:
        response = requests.get(f"{URL}/notes/?category={category.lower()}")

    if response.status_code == 200:
        return response.json()
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
    """Parse habr posts with this category and return them formatted (+desc)"""
    response = requests.get(f"{URL}/habr/get_posts/?category={category}")
    if response.status_code == 200:
        data = response.json()
        if data:
            posts_list = [
                f"views: {post['views']}\nvotes: {post['votes']}\n\n{post['url']}"
                for post in data
            ]
            return posts_list[::-1]
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
