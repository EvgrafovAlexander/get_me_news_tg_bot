from logger import logger

MAX_LENGTH = 4000


def build_news_messages(source_name: str, news_list: list) -> list:
    """
    Создаёт перечень сообщений на отправку подписчикам.

    :param source_name: источник статей
    :param news_list: перечень статей, полученных из источника
    :return: перечень сообщений на отправку
    """
    messages = []

    message = f"<b>Последние новости с {source_name}:</b>\n\n"
    if not news_list:
        logger.info(f"Empty news list, source: {source_name}")
        return messages
    for news in news_list:
        line = f"• <a href=\"{news['link']}\">{news['title']}</a> ({news['published_date']})\n\n"
        if len(message) + len(line) > MAX_LENGTH:
            messages.append(message)
            message = f"<b>Последние новости с {source_name} - продолжение:</b>\n\n"
        message += f"• <a href=\"{news['link']}\">{news['title']}</a> ({news['published_date']})\n\n"
    messages.append(message)
    return messages
