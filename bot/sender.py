from telegram import Bot
from telegram.request import HTTPXRequest

from config.settings import settings
from logger import logger


class BotSender:
    def __init__(self):
        request = HTTPXRequest(proxy=settings.telegram_proxy)
        self.bot = Bot(token=settings.bot_token, request=request)

    async def broadcast(self, messages: list[str]):
        """
        Публикует сообщения в новостном канале.

        :param messages: перечень сообщений на отправку
        """
        for message in messages:
            try:
                await self.bot.send_message(
                    chat_id=settings.channel_id,
                    text=message,
                    parse_mode="HTML"
                )
            except Exception as e:
                logger.error(f"Ошибка публикации в канал {settings.channel_id}: {e}")
