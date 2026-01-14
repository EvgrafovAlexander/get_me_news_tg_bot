from bot.sender import BotSender
from logger import logger
from news.formatter import build_news_messages
from news.http_client import RSSHttpClient
from news.parser import RSSParser
from news.reader import NewsReader
from news.rss_sources import RSS_SOURCES
from services.articles import ArticleService
from services.db import cleanup_old_articles


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

            reader = NewsReader(http_client=RSSHttpClient(), parser=RSSParser())
            articles = reader.read(url)
            filtered_articles = ArticleService.filter_new_only(articles=articles)

            messages = build_news_messages(name, filtered_articles)
            await BotSender().broadcast(messages)

            ArticleService.mark_articles_as_checked(filtered_articles)

        except Exception as e:
            logger.error(f"Error processing source: {source['name']}, description: {e}")
    logger.info("RSS check finished.")


async def weekly_cleanup_job():
    logger.info("Weekly cleanup running...")
    cutoff = cleanup_old_articles()
    logger.info(f"Weekly cleanup finished. Removed articles older than {cutoff}")
