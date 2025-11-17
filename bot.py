from telegram import Bot

import os


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


async def send_message_to_bot(text):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode="HTML")


def create_messages_from_news(source_name: str, news_list: list) -> list:
    MAX_LENGTH = 4000
    messages = []

    message = f"<b>Последние новости с {source_name}:</b>\n\n"
    if not news_list:
        message += "свежих новостей не найдено."
    for news in news_list:
        line = f"• <a href=\"{news['link']}\">{news['title']}</a> ({news['published_date']})\n\n"
        if len(message) + len(line) > MAX_LENGTH:
            messages.append(message)
            message = f"<b>Последние новости с {source_name} - продолжение:</b>\n\n"
        message += f"• <a href=\"{news['link']}\">{news['title']}</a> ({news['published_date']})\n\n"
    messages.append(message)
    return messages
