from bot import send_message_to_bot, create_messages_from_news
from db import cleanup_old_articles
from logger import logger
from news import get_news_from_source
from rss_sources import RSS_SOURCES


async def run_bot(app):
    logger.info("Telegram bot initializing...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logger.info("Telegram bot polling started.")


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


async def weekly_cleanup_job():
    logger.info("Weekly cleanup running...")
    cutoff = cleanup_old_articles()
    logger.info(f"Weekly cleanup finished. Removed articles older than {cutoff}")
