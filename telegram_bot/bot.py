import os

import telebot
from telebot import types

from dotenv import load_dotenv

from services import (
    get_habr_posts,
    send_posts,
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
        
        /week
    costs:
        /daily_costs
        /del_cost (name) 
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
        send_posts(bot, message, posts)

    elif message.text.startswith("/week") and len(message.text) < 7:
        posts = get_habr_posts(category="top_weekly")
        send_posts(bot, message, posts)

    elif message.text == "> 10 posts":
        posts = get_habr_posts(category="with_rating")
        send_posts(bot, message, posts)

    elif message.text.startswith("/"):
        pass

    elif message.text.startswith(""):
        pass

    elif message.text.startswith(""):
        pass

    elif message.text.startswith(""):
        pass

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
