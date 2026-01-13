from bot.sender import BotSender
from core.news_formatter import build_news_messages
from core.news_reader import get_news_from_source
from core.rss_sources import RSS_SOURCES
from db import cleanup_old_articles
from logger import logger


async def run_bot(app):
    logger.info("Telegram bot initializing...")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    logger.info("Telegram bot polling started.")


async def check_all_sources():
    logger.info("RSS check running...")
    for source in RSS_SOURCES:
        try:
            url = source['url']
            name = source['name']

            news = get_news_from_source(url)
            messages = build_news_messages(name, news)
            await BotSender().broadcast(messages)
        except Exception as e:
            logger.error(f"Error processing source: {source['name']}, description: {e}")
    logger.info("RSS check finished.")


async def weekly_cleanup_job():
    logger.info("Weekly cleanup running...")
    cutoff = cleanup_old_articles()
    logger.info(f"Weekly cleanup finished. Removed articles older than {cutoff}")
