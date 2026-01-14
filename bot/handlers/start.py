from telegram import Update
from telegram.ext import ContextTypes

from logger import logger
from services.subscribers import SubscriberService


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start
    """
    chat_id = str(update.effective_chat.id)

    try:
        SubscriberService.subscribe(chat_id)

        await update.message.reply_text(
            "Вы подписались на обновления! 📰\n"
            "Чтобы отписаться, используйте команду /stop ."
        )
    except Exception:
        logger.exception(
            f"Failed 'start' handler"
        )
        await update.message.reply_text(
            "Произошла ошибка 😞 Попробуйте позже."
        )
