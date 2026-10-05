from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.request import HTTPXRequest

from bot.handlers import start, stop
from config.settings import settings


def create_bot_app():
    request = HTTPXRequest(proxy=settings.telegram_proxy)
    get_updates_request = HTTPXRequest(proxy=settings.telegram_proxy)
    app = (
        ApplicationBuilder()
        .token(settings.bot_token)
        .request(request)
        .get_updates_request(get_updates_request)
        .build()
    )

    app.add_handler(CommandHandler("start", start.start))
    app.add_handler(CommandHandler("stop", stop.stop))

    return app
