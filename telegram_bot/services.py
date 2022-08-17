import calendar
import datetime
from datetime import date
from typing import NamedTuple, Optional, List, TypedDict, Union

import requests

from telebot import TeleBot
from telebot.types import Message


URL = "https://maksimburtsev.pythonanywhere.com/"


class NoteDict(TypedDict):
    pk: int
    name: str
    description: Optional[str]
    date: str
    category: Optional[str]


class MonthStartEndDates(NamedTuple):
    start_date: str
    end_date: str


def create_purchases(raw_purchases: List[str]) -> bool:
    """Create json with purchases and make POST request"""
    today_date = str(date.today())
    purchases_list = []

    for i in range(0, len(raw_purchases), 2):
        purchases_list.append(
            {"name": raw_purchases[i], "cost": raw_purchases[i + 1], "date": today_date}
        )
    response = requests.post(f"{URL}/purchases/", json=purchases_list)
    return response.status_code == 201


def get_notes(query: Optional[str]) -> List[Optional[str]]:
    """Return list of formatted notes on this query"""
    if query:
        raw_notes = _get_notes(category=query)
        if not raw_notes:
            raw_notes = _get_notes(name=query)
    else:
        raw_notes = _get_notes()

    notes_list = []
    for note in raw_notes:
        note = _format_note(note)
        notes_list.append(note)

    return notes_list


def _format_note(note: NoteDict) -> str:
    """Format note dict into a str"""
    res = note["name"]

    if note["description"]:
        res += f"\n{note['description']}"

    note_date = note["date"][:10]
    if note["category"]:
        res += f"\n\n{note['category']}, {note_date}"
    else:
        res += f"\n\n{note_date}"

    return res


def delete_notes(query: str) -> bool:
    """Delete notes with query. First GET pk of notes with name and category, which contains query. Second is DELETE them"""
    if not query: return False

    with_name = [note["pk"] for note in _get_notes(name=query) if note]
    with_category = [note["pk"] for note in _get_notes(category=query) if note]

    pk_notes_for_delete = set(with_name + with_category)

    if pk_notes_for_delete:
        for pk in pk_notes_for_delete:
            requests.delete(f"{URL}/notes/{pk}/")
        return True
    return False


def _get_notes(
    name: Optional[str] = None, category: Optional[str] = None
) -> Union[NoteDict, dict]:
    """GET notes with name | category. If both empty return all notes from database"""
    if name:
        response = requests.get(f"{URL}/notes/?name={name.title()}")
    elif category:
        response = requests.get(f"{URL}/notes/?category={category.lower()}")
    else:
        response = requests.get(f"{URL}/notes/")

    if response.status_code == 200:
        return response.json()
    return []


def create_note(
    name: str, category: Optional[str] = None, description: Optional[str] = None
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


def send_purchases(bot: TeleBot, message: Message, purchases_list: List[str]) -> None:
    """Send list of purchases"""
    if purchases_list:
        for purchase in purchases_list:
            bot.send_message(message.chat.id, purchase)
        return
    else:
        return bot.send_message(message.chat.id, "purchasts list is empty")


def get_current_month_dates() -> MonthStartEndDates:
    """Return first and last day (in date format) of current month"""
    today_date = date.today()
    year, month = today_date.year, today_date.month

    last_day = calendar.monthrange(year, month)[-1]

    return MonthStartEndDates(f"{year}-{month}-01", f"{year}-{month}-{last_day}")


def get_purchases_report(from_date: str = "", to_date: str = "") -> List[str]:
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
    return []

if __name__ == "__main__":
    print(_get_notes())