from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import os

from db import add_subscriber, get_all_subscribers, remove_subscriber
from logger import logger

BOT_TOKEN = os.getenv("BOT_TOKEN")


def create_bot_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    return app


async def send_message_to_bot(text):
    bot = Bot(token=BOT_TOKEN)
    subscribers = get_all_subscribers()
    for chat_id in subscribers:
        try:
            await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
        except Exception as e:
            logger.error(f"Ошибка отправки {chat_id}: {e}")


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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start
    """
    chat_id = str(update.effective_chat.id)
    add_subscriber(chat_id)

    await update.message.reply_text(
        "Вы подписались на обновления! 📰\n"
        "Чтобы отписаться, используйте команду /stop ."
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /stop
    """
    chat_id = str(update.effective_chat.id)
    remove_subscriber(chat_id)

    await update.message.reply_text(
        "Вы отписались от рассылки. 👋\n"
        "Чтобы подписаться заново, используйте команду /start ."
    )
