import feedparser

from logger import logger


class RSSParser:

    def parse(self, content: bytes, source_url: str) -> list[dict]:
        feed = feedparser.parse(content)

        if feed.bozo:
            logger.warning(
                f"Invalid RSS feed | source={source_url} | error={feed.bozo_exception}"
            )

        articles = []

        for entry in feed.entries:
            article = self._parse_entry(entry, source_url)
            if article:
                articles.append(article)

        return articles

    def _parse_entry(self, entry, source_url: str) -> dict | None:
        try:
            title, link = entry.title, entry.link
            published_date, parsed_published_date = entry.published, entry.published_parsed

            return {
                "source_url": source_url,
                "title": title,
                "link": link,
                "published_date": published_date,
                "parsed_published_date": parsed_published_date,
            }
        except Exception:
            logger.exception(
                f"Failed to process RSS entry | source={source_url} | "
                f"title={getattr(entry, 'title', None)} | "
                f"link={getattr(entry, 'link', None)}"
            )
            return None
