import os

import telebot
from telebot import types

from dotenv import load_dotenv


load_dotenv()

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
        /daily_costs
        /del_cost (name) 
    notes:
        /note [category] - create note
        /del (pk)
        /get_notes [category | name | None]
    """
    bot.send_message(chat_id=message.chat.id, text=text)

bot.infinity_polling()
