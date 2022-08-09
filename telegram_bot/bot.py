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
)


load_dotenv()

MY_ID = int(os.getenv("MY_ID"))
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("monthly costs")
    item2 = types.KeyboardButton("> 10 posts")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, "hi", reply_markup=markup)


@bot.message_handler(commands=["help"])
def help(message):
    text = """
    Commads:
    posts:
        /today
        /week
    costs:
        /daily_purchases
        /del_purchase (name) 
        /month_purchases (month) (year | None)
    notes:
        /note [category] - create note
        /del (pk)
        /get_notes [category | name | None]
    """
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(content_types="text")
def main(message):

    chat_id = message.chat.id

    if chat_id != MY_ID:
        return bot.send_message(chat_id, "forbidden")

    if message.text.startswith("/today") and len(message.text) < 10:
        posts = get_habr_posts()
        return send_posts(bot, message, posts)

    elif message.text.startswith("/week") and len(message.text) < 7:
        posts = get_habr_posts(category="top_weekly")
        return send_posts(bot, message, posts)

    elif message.text == "> 10 posts":
        posts = get_habr_posts(category="with_rating")
        return send_posts(bot, message, posts)

    elif message.text.startswith("/daily_purchases"):
        date_today = str(datetime.datetime.now().date())
        purchases_list = get_purchases_report(from_date=date_today)
        return send_purchases(bot, message, purchases_list)

    elif message.text.startswith("monthly costs"):
        first_day, last_day = get_current_month_dates()
        purchases_list = get_purchases_report(first_day, last_day)
        return send_purchases(bot, message, purchases_list)

    elif message.text.startswith("/del_purchase") and len(message.text.split()) == 2:

        res = remove_purchase(name=message.text.split()[1])
        if res:
            return bot.send_message(chat_id, "success")
        else:
            return bot.send_message(chat_id, "404")

    elif (
        message.text.startswith("/month_purchases")
        and 2 <= len(message.text.split()) <= 3
    ):

        input_data = message.text.split()

        year = datetime.date.today().year if len(input_data) == 2 else input_data[2]
        month = input_data[1]

        res = get_monthly_costs(month, year)

        return bot.send_message(chat_id, res)

    elif message.text == "/note":
        text = """structure of message:\n\n /node (category | None)\n name\n description | None"""
        return bot.send_message(chat_id, text)

    elif message.text.startswith("/note") and len(message.text.split("\n")) >= 2:

        data = message.text.split("\n")
        category = None if len(data[0].split()) != 2 else data[0].split()[1]
        name = data[1]
        description = None if len(data) != 3 else data[2]

        res = create_note(name, category, description)

        response_text = "Success" if res else "Something wrong..."

        bot.send_message(chat_id, response_text)

    elif message.text.startswith(""):
        pass

    elif message.text.startswith(""):
        pass

    elif message.text.startswith(""):
        pass

    else:
        # TODO try to add cost
        pass


bot.infinity_polling()
