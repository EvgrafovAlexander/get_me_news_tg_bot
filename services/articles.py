from config.settings import settings
from services.db import is_article_new, mark_article_as_checked
from logger import logger


class ArticleService:
    @staticmethod
    def filter_new_only(articles: list[dict]):
        filtered_articles = []

        for article in articles:
            try:
                if is_article_new(article["link"], article["parsed_published_date"], settings.rss_last_days):
                    filtered_articles.append(article)

            except Exception:
                logger.exception(
                    f"Failed to filter article | article={article}"
                )

        return filtered_articles

    @staticmethod
    def mark_articles_as_checked(articles: list[dict]):
        for article in articles:
            try:
                mark_article_as_checked(article["link"], article["title"], article["published_date"])
            except Exception:
                logger.exception(
                    f"Failed to mark_articles_as_checked | article={article}"
                )
