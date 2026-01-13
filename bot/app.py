from telegram.ext import ApplicationBuilder, CommandHandler

from bot.handlers import start, stop
from config.settings import settings


def create_bot_app():
    app = ApplicationBuilder().token(settings.bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    return app
