from telegram import Update
from telegram.ext import ContextTypes

from services.subscribers import SubscriberService


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /start
    """
    chat_id = str(update.effective_chat.id)
    SubscriberService.subscribe(chat_id)

    await update.message.reply_text(
        "Вы подписались на обновления! 📰\n"
        "Чтобы отписаться, используйте команду /stop ."
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Обработчик команды /stop
    """
    chat_id = str(update.effective_chat.id)
    SubscriberService.unsubscribe(chat_id)

    await update.message.reply_text(
        "Вы отписались от рассылки. 👋\n"
        "Чтобы подписаться заново, используйте команду /start ."
    )
