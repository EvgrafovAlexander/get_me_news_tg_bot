from telegram import Bot

import os

from logger import logger

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_IDS = os.getenv("CHAT_IDS").split(",")


async def send_message_to_bot(text):
    bot = Bot(token=BOT_TOKEN)
    for chat_id in CHAT_IDS:
        await bot.send_message(chat_id=chat_id.strip(), text=text, parse_mode="HTML")


def create_messages_from_news(source_name: str, news_list: list) -> list:
    MAX_LENGTH = 4000
    messages = []

    message = f"<b>Последние новости с {source_name}:</b>\n\n"
    if not news_list:
        logger.info(f"Empty news list, source: {source_name}")
        return messages
    for news in news_list:
        line = f"• <a href=\"{news['link']}\">{news['title']}</a> ({news['published_date']})\n\n"
        if len(message) + len(line) > MAX_LENGTH:
            messages.append(message)
            message = f"<b>Последние новости с {source_name} - продолжение:</b>\n\n"
        message += f"• <a href=\"{news['link']}\">{news['title']}</a> ({news['published_date']})\n\n"
    messages.append(message)
    return messages
