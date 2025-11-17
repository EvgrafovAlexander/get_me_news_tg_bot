import asyncio

from bot import send_message_to_bot, create_messages_from_news
from news import get_news_from_source
from rss_sources import RSS_SOURCES


if __name__ == "__main__":
    for source in RSS_SOURCES:
        url = source['url']
        name = source['name']

        news = get_news_from_source(url)
        messages = create_messages_from_news(name, news)
        for message in messages:
            asyncio.run(send_message_to_bot(message))
