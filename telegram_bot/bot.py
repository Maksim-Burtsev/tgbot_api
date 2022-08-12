import os
import datetime

import telebot
from telebot import types

from dotenv import load_dotenv

from services import (
    get_habr_posts,
    send_posts,
    get_purchases_report,
    get_current_month_dates,
    send_purchases,
    remove_purchase,
    get_monthly_costs,
    create_note,
    delete_notes,
    get_notes,
    create_purchases,
)


load_dotenv()

MY_ID = int(os.getenv("MY_ID"))
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("monthly costs")
    item2 = types.KeyboardButton("daily posts")
    markup.add(item1)
    markup.add(item2)

    return bot.send_message(message.chat.id, "hi", reply_markup=markup)


@bot.message_handler(commands=["help"])
def help_(message):
    text = """
    Commads:
    posts:
        /rating
        /week
    costs:
        /daily_purchases
        /del_purchase (name) 
        /month_purchases (month) (year | None)
    notes:
        /note - structure of creating note
        /note [category] - create note
        /del_note (pk)
        /get_notes [category | name | None]
    """
    return bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(content_types="text")
def main(message):

    chat_id = message.chat.id
    text = message.text

    if chat_id != MY_ID:
        return bot.send_message(chat_id, "forbidden")

    if text == ("daily posts"):
        posts = get_habr_posts()
        return send_posts(bot, message, posts)

    elif text.startswith("/week") and len(text) < 7:
        posts = get_habr_posts(category="top_weekly")
        return send_posts(bot, message, posts)

    elif text == "/rating" and len(text) < 10:
        posts = get_habr_posts(category="with_rating")
        return send_posts(bot, message, posts)

    elif text.startswith("/daily_purchases"):
        date_today = str(datetime.datetime.now().date())
        purchases_list = get_purchases_report(from_date=date_today)
        return send_purchases(bot, message, purchases_list)

    elif text.startswith("monthly costs"):
        first_day, last_day = get_current_month_dates()
        purchases_list = get_purchases_report(first_day, last_day)
        return send_purchases(bot, message, purchases_list)

    elif text.startswith("/del_purchase") and len(text.split()) == 2:

        name = text.split()[1]
        res = remove_purchase(name)

        if res:
            return bot.send_message(chat_id, "success")
        else:
            return bot.send_message(chat_id, "404")

    elif text.startswith("/month_purchases") and 2 <= len(text.split()) <= 3:

        input_data = text.split()

        year = datetime.date.today().year if len(input_data) == 2 else input_data[2]
        month = input_data[1]

        res = get_monthly_costs(month, year)
        return bot.send_message(chat_id, res)

    elif text == "/note":
        text = """structure of message:\n\n /node (category | None)\n name\n description | None"""
        return bot.send_message(chat_id, text)

    elif text.startswith("/note") and len(text.split("\n")) >= 2:

        data = text.split("\n")
        category = None if len(data[0].split()) != 2 else data[0].split()[1]
        name = data[1]
        description = None if len(data) != 3 else data[2]

        res = create_note(name, category, description)

        response_text = "Success" if res else "Something wrong..."
        return bot.send_message(chat_id, response_text)

    elif text.startswith("/del_note") and len(text.split()) == 2:
        query = text.split()[1]
        res = delete_notes(query)
        response_text = "Success" if res else "Something wrong..."
        return bot.send_message(chat_id, response_text)

    elif text.startswith("/get_notes") and len(text.split()) == 2:
        query = text.split()[1]
        notes = get_notes(query)

        if notes:
            for note in notes:
                bot.send_message(chat_id, note)

    elif len(text.split()) % 2 == 0:
        raw_purchases = text.split()

        if all([price.isdigit() for price in raw_purchases[1::2]]):
            res = create_purchases(raw_purchases)
            response_text = "Success" if res else "Opppppsss..."
            return bot.send_message(chat_id, response_text)

        return bot.send_message(chat_id, "cost must be digit")



if __name__ == "__main__":
    bot.infinity_polling()
