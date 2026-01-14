from telegram import Update
from telegram.ext import ContextTypes

from logger import logger
from services.subscribers import SubscriberService


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /stop
    """
    chat_id = str(update.effective_chat.id)

    try:
        SubscriberService.unsubscribe(chat_id)

        await update.message.reply_text(
            "Вы отписались от рассылки. 👋\n"
            "Чтобы подписаться заново, используйте команду /start ."
        )
    except Exception:
        logger.exception(
            f"Failed 'stop' handler"
        )
        await update.message.reply_text(
            "Произошла ошибка 😞 Попробуйте позже."
        )
