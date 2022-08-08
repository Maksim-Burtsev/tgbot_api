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
        /month_purchases (month) (year | None)
        /del_purchase (name) 
    notes:
        /note [category] - create note
        /del (pk)
        /get_notes [category | name | None]
    """
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(content_types="text")
def main(message):

    if message.chat.id != MY_ID:
        return bot.send_message(message.chat.id, "forbidden")

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

    elif message.text.startswith("/del_purchase") and \
         len(message.text.split()) == 2:
         
        res = remove_purchase(name=message.text.split()[1])
        if res:
            return bot.send_message(message.chat.id, "success")
        else:
            return bot.send_message(message.chat.id, "404")

    elif message.text.startswith("/month_purchases") and \
         len(message.text.split()) in [2,3,]:

        input_data = message.text.split()

        year = datetime.date.today().year if len(input_data) == 2 else input_data[2]
        month = input_data[1]

        res = get_monthly_costs(month, year)

        return bot.send_message(message.chat.id, res)

    elif message.text.startswith(""):
        pass

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
