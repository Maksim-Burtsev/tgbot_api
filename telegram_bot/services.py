import os

import requests
from dotenv import load_dotenv

from telebot import TeleBot
from telebot.types import Message


load_dotenv()
URL = os.getenv("URL")

def send_posts(bot: TeleBot, message: Message, posts: list[str]) -> None:
    if posts:
        for post in posts:
            bot.send_message(message.chat.id, post)


def get_habr_posts(category: str | None = None) -> list[str | None]:
    response = requests.get(
        f"{URL}/habr/get_posts/?category={category}"
    )
    if response.status_code == 200:
        data = response.json()
        if data:
            posts_list = [
                f"views:{post['views']}\nvotes:{post['votes']}\n\n{post['url']}"
                for post in data
            ]
            return posts_list
    return []


if __name__ == "__main__":
    print(type(os.getenv('URL')))