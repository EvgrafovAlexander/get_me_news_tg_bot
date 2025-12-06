import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from bot import send_message_to_bot, create_bot_app, create_messages_from_news
from db import init_db
from logger import logger
from news import get_news_from_source
from rss_sources import RSS_SOURCES


async def check_all_sources():
    logger.info("RSS check running...")
    for source in RSS_SOURCES:
        url = source['url']
        name = source['name']

        news = get_news_from_source(url)
        messages = create_messages_from_news(name, news)

        for message in messages:
            await send_message_to_bot(message)
    logger.info("RSS check finished.")


async def run_bot(app):
    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    logger.info("Telegram bot polling started.")


async def run_scheduler():
    """Запускает APScheduler с выполнением периодической задачи check_all_sources"""
    refresh_minutes = int(os.getenv("RSS_REFRESH_MINUTES", 20))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_all_sources, "interval", minutes=refresh_minutes)
    scheduler.start()

    logger.info(f"Scheduler started with interval: {refresh_minutes} minutes.")


async def main():
    # Создаем и запускаем экземпляр бота
    bot_app = create_bot_app()
    asyncio.create_task(run_bot(bot_app))

    # Запускаем APScheduler с задачей check_all_sources
    asyncio.create_task(run_scheduler())

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    load_dotenv()
    init_db()
    if os.getenv("MANUAL_RUN", False):
        logger.info("MANUAL_RUN enabled — running check_all_sources once.")
        asyncio.run(check_all_sources())
    else:
        asyncio.run(main())
