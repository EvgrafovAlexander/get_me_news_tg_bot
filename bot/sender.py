from telegram import Bot

from config.settings import settings
from logger import logger
from services.subscribers import SubscriberService


class BotSender:
    def __init__(self):
        self.bot = Bot(token=settings.bot_token)

    async def broadcast(self, messages: list[str]):
        """
        Отправляет сообщения подписчикам бота.

        :param messages: перечень сообщений на отправку
        """
        subscribers = SubscriberService.get_all()

        for chat_id in subscribers:
            for message in messages:
                try:
                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=message,
                        parse_mode="HTML"
                    )
                except Exception as e:
                    logger.error(f"Ошибка отправки {chat_id}: {e}")
