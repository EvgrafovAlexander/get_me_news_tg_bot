import asyncio
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from bot import send_message_to_bot, create_messages_from_news
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


async def main():
    load_dotenv()

    refresh_minutes = int(os.getenv("RSS_REFRESH_MINUTES", 20))

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_all_sources, "interval", minutes=refresh_minutes)
    scheduler.start()

    logger.info(f"Scheduler started with {refresh_minutes} minutes interval.")

    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
